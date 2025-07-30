import re

def replace_delete_insert_with_overwrite(sql_blocks):
    cleaned_blocks = [] 
    skip_next = False 

    for i in range(len(sql_blocks)): 
        if skip_next:
            skip_next = False 
            continue

        current_block = sql_blocks[i].strip()
        next_block = sql_blocks[i + 1].strip() if i + 1 < len(sql_blocks) else "" 

        delete_match = re.match(r'^DELETE\s+FROM\s+([^\s;]+);?$', current_block, re.IGNORECASE)
        insert_match = re.match(
            r'^INSERT\s+INTO\s+([^\s(]+)(\s*\([^)]+\))?\s+(SELECT.+);?$',
            next_block,
            re.IGNORECASE | re.DOTALL
        )

        if delete_match and insert_match:
            delete_table = delete_match.group(1)
            insert_table = insert_match.group(1)

            if delete_table.lower() == insert_table.lower():
                columns_part = insert_match.group(2) or ""
                select_part = insert_match.group(3)
                overwrite_sql = f"INSERT OVERWRITE {insert_table}{columns_part} {select_part};"
                cleaned_blocks.append(overwrite_sql)
                skip_next = True
                continue

        cleaned_blocks.append(current_block)

    return cleaned_blocks

def replace_update_insert_with_merge(sql_blocks):
    """
    Replace pairs of UPDATE + INSERT INTO statements on the same table with a single MERGE statement.
    Maintains proper formatting and indentation for Spark SQL.
    """

    merged_blocks = []
    skip_next = False

    for i in range(len(sql_blocks)):
        if skip_next:
            skip_next = False
            continue

        current_block = sql_blocks[i].strip()
        next_block = sql_blocks[i+1].strip() if i + 1 < len(sql_blocks) else ""

        # Match UPDATE with FROM (SELECT * FROM staging WHERE DW_ERR <> 'Y') STG SET ... WHERE ...
        update_pattern = (
            r'^UPDATE\s+([\$\{\}\w\.]+)\s+FROM\s+\(SELECT\s+\*\s+FROM\s+([\$\{\}\w\.]+)\s+WHERE\s+DW_ERR\s*<>\s*\'Y\'\)\s+STG\s+SET\s+(.+?)\s+WHERE\s+(.+);?$'
        )
        update_match = re.match(update_pattern, current_block, re.IGNORECASE | re.DOTALL)

        # Match INSERT INTO same target table with columns and SELECT from STG with LEFT JOIN
        insert_pattern = (
            r'^INSERT\s+INTO\s+([\$\{\}\w\.]+)\s*\(([\s\S]+?)\)\s*SELECT\s+([\s\S]+?)\s+FROM\s+\(.*\)\s+STG\s+LEFT\s+JOIN\s+.+$'
        )
        insert_match = re.match(insert_pattern, next_block, re.IGNORECASE | re.DOTALL)

        if update_match and insert_match:
            update_table = update_match.group(1).lower()
            staging_table_from_update = update_match.group(2)
            set_clause = update_match.group(3).strip()
            where_clause = update_match.group(4).strip()

            insert_table = insert_match.group(1).lower()
            insert_cols_raw = insert_match.group(2).strip()
            insert_select_raw = insert_match.group(3).strip()

            if update_table == insert_table:
                # Parse ON condition columns from WHERE clause (target.col = STG.col)
                on_conditions = []
                for cond in re.split(r'\s+AND\s+', where_clause, flags=re.IGNORECASE):
                    m = re.match(r'([\$\{\}\w\.]+)\s*=\s*STG\.([\w_]+)', cond.strip(), re.IGNORECASE)
                    if m:
                        tgt_col = m.group(1).split('.')[-1]
                        stg_col = m.group(2)
                        on_conditions.append(f"target.{tgt_col} = source.{stg_col}")
                on_clause = " AND\n    ".join(on_conditions)

                # Parse SET assignments (col = STG.col)
                set_assignments = []
                for assign in re.split(r',\s*(?=[\w_]+\s*=)', set_clause):
                    m = re.match(r'([\w_]+)\s*=\s*STG\.([\w_]+)', assign.strip())
                    if m:
                        tgt_col = m.group(1)
                        stg_col = m.group(2)
                        set_assignments.append(f"{tgt_col} = source.{stg_col}")

                set_clause_str = ",\n    ".join(set_assignments)

                # Prepare INSERT columns and values
                insert_cols = [c.strip() for c in insert_cols_raw.split(',')]
                insert_values = [f"source.{c}" for c in insert_cols]

                merge_sql = f"""MERGE INTO {update_table} AS target
USING (
    SELECT * FROM {staging_table_from_update} WHERE DW_ERR <> 'Y'
) AS source
ON {on_clause}
WHEN MATCHED THEN
  UPDATE SET
    {set_clause_str}
WHEN NOT MATCHED THEN
  INSERT ({', '.join(insert_cols)})
  VALUES ({', '.join(insert_values)})
;"""

                merged_blocks.append(merge_sql)
                skip_next = True
                continue

        merged_blocks.append(current_block)

    return merged_blocks


def convert_update_where_in_group_by_to_merge(sql_code):
    """
    Generic conversion of UPDATE ... SET ... WHERE (cols) IN (SELECT cols FROM same table GROUP BY cols HAVING COUNT(*)>1)
    to a Spark MERGE statement.
    """

    pattern = re.compile(
        r"""
        UPDATE\s+(\S+)\s+            # table name after UPDATE
        SET\s+(\S+)\s*=\s*(.+?)\s+  # SET <column> = <value>
        WHERE\s*\(\s*([^)]+)\s*\)\s*IN\s*\(  # WHERE (<cols>) IN (
        \s*SELECT\s+\4\s+            # SELECT same columns as in WHERE tuple
        FROM\s+\1\s+                 # FROM same table
        GROUP\s+BY\s+\4\s+           # GROUP BY same columns
        HAVING\s+COUNT\s*\(\*\)\s*>\s*1\s*   # HAVING COUNT(*) > 1
        \)\s*;?                     # closing bracket and optional semicolon
        """,
        re.IGNORECASE | re.VERBOSE | re.DOTALL
    )

    def _convert(match):
        table = match.group(1)
        set_col = match.group(2)
        set_val = match.group(3).strip()
        cols_str = match.group(4).strip()

        cols = [c.strip() for c in cols_str.split(',')]

        on_conditions = " AND ".join([f"target.{c} = src.{c}" for c in cols])

        merge_sql = f"""
MERGE INTO {table} AS target
USING (
    SELECT {cols_str}
    FROM {table}
    GROUP BY {cols_str}
    HAVING COUNT(*) > 1
) AS src
ON {on_conditions}
WHEN MATCHED THEN
  UPDATE SET {set_col} = {set_val}
""".strip()

        return merge_sql

    return pattern.sub(_convert, sql_code)


def code_cleanup_bteq(input_file, output_file):
    unix_keywords = (
        '.', 'if', '*', 'fi', 'echo', '#!', 'RC', 'EOF', 'return',
        'bteq', 'EXEC', '.OS', '.LOGON', '.LOGOFF', '.QUIT', 'BT', 'ET', 'SET QUERY'
    )

    sql_lines = []
    sql_block = []

    with open(input_file, 'r') as f:
        for line in f:
            stripped = line.strip()

            if (
                not stripped or
                stripped.startswith('--') or
                stripped.startswith('#') or
                stripped.startswith('/*') or
                any(stripped.startswith(k) for k in unix_keywords)
            ):
                continue

            sql_block.append(line.rstrip())

            if stripped.endswith(';'):
                sql_code = '\n'.join(sql_block)
                sql_lines.append(sql_code.strip())
                sql_block = []

    # Replace DELETE + INSERT → INSERT OVERWRITE
    sql_lines = replace_delete_insert_with_overwrite(sql_lines)

    # Replace UPDATE + INSERT → MERGE
    sql_lines = replace_update_insert_with_merge(sql_lines)

    cleaned_sql_lines = []
    for sql_query in sql_lines:
        # Generic UPDATE WHERE IN GROUP BY to MERGE
        sql_query = convert_update_where_in_group_by_to_merge(sql_query)

        upper_query = sql_query.upper()

        # Skip volatile tables and stats/utility queries
        if any(upper_query.startswith(prefix) for prefix in [
            'CREATE MULTISET VOLATILE TABLE VT_STEP_ACTVTY',
            'INSERT INTO VT_STEP_ACTVTY',
            'CREATE MULTISET VOLATILE TABLE VT_DT_PRM2',
            'INSERT INTO VT_DT_PRM2',
            'SELECT CURRENT_TIMESTAMP(0);',
            'COLLECT STATS INDEX(MYBTCH_ID,MYSTEP_ID,STEP_STRT_DTM) ON VT_STEP_ACTVTY;'
        ]):
            continue

        # Remove LEFT JOIN VT_STEP_ACTVTY
        modified_sql = re.sub(
            r'LEFT\s+OUTER\s+JOIN\s+VT_STEP_ACTVTY\s+ON\s+1=1',
            '',
            sql_query,
            flags=re.IGNORECASE
        )

        # Replace specific aliases with NULL
        modified_sql = re.sub(
            r'MYBTCH_ID\s+AS\s+DW_BTCH_ID',
            'NULL AS DW_BTCH_ID',
            modified_sql, 
            flags=re.IGNORECASE
        )
        modified_sql = re.sub(
            r'MYSTEP_ID\s+AS\s+DW_STEP_ID',
            'NULL AS DW_STEP_ID',
            modified_sql,
            flags=re.IGNORECASE
        )

        modified_sql = re.sub(r'SEL ', 'SELECT ',modified_sql, flags=re.IGNORECASE)
        modified_sql = re.sub(r'\$', '',modified_sql, flags=re.IGNORECASE)

        # Wrap in spark.sql
        wrapped_sql = f'spark.sql("""\n{modified_sql}\n""")\n'
        cleaned_sql_lines.append(wrapped_sql)


    with open(output_file, 'w') as f:
        f.writelines(cleaned_sql_lines)

    print(f" Cleanup completed. Converted SQL written to:\n{output_file}")
 

input_file = 'C:/Users/2148016/Downloads/sql_file.btq'
output_file = 'C:/Users/2148016/Downloads/sql_file.py'

code_cleanup_bteq(input_file,output_file)
