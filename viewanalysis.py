import pandas as pd
# from pandas import DataFrame
import re
# import xlsxwriter
import ExcelToList
import connect_td_ssh as td

def remove_sql_comments(sql_text):
    """
    Remove SQL comments (-- single line and /* */ multi-line) from SQL text.
    Handles separator lines (lines of only dashes) that are not actual comments.
    
    Args:
        sql_text (str): Raw SQL text
    
    Returns:
        str: SQL text with comments removed
    """
    # Remove multi-line comments /* ... */
    sql_text = re.sub(r'/\*.*?\*/', '', sql_text, flags=re.DOTALL)
    
    # Remove single-line comments -- ...
    # Handle different line endings: \r\n, \n, or \r
    lines = re.split(r'\r\n|\n|\r', sql_text)
    cleaned_lines = []
    for line in lines:
        # Skip lines that are only dashes and whitespace (separator lines)
        if re.match(r'^[-\s\r]*$', line):
            continue  # Skip separator lines entirely
        
        # Find -- comment marker (not inside quotes)
        comment_pos = -1
        in_single_quote = False
        in_double_quote = False
        
        i = 0
        while i < len(line) - 1:
            if line[i] == "'" and not in_double_quote:
                in_single_quote = not in_single_quote
            elif line[i] == '"' and not in_single_quote:
                in_double_quote = not in_double_quote
            elif line[i:i+2] == '--' and not in_single_quote and not in_double_quote:
                # Additional check: make sure this isn't just a line of dashes
                # Real comments usually have text after --
                rest_of_line = line[i+2:].strip()
                if not re.match(r'^[-\s]*$', rest_of_line):  # Has content after --
                    comment_pos = i
                    break
                # If it's just dashes, continue looking for real comments
            i += 1
        
        if comment_pos >= 0:
            cleaned_lines.append(line[:comment_pos])
        else:
            cleaned_lines.append(line)
    
    return ' '.join(cleaned_lines)

def get_object_names(view):
    """
    Extract table/view names from SQL view definition, properly handling comments.
    
    Args:
        view: View definition (list of lists or string)
    
    Returns:
        list: List of table/view names found in FROM/JOIN clauses
    """
    # Convert view to string if it's nested lists
    if isinstance(view, list):
        sql_text = ''
        for j in view:
            if isinstance(j, list):
                for i in j:
                    sql_text += str(i) + ' '
            else:
                sql_text += str(j) + ' '
    else:
        sql_text = str(view)
    
    print(f"DEBUG - Original SQL: {repr(sql_text[:2000])}...")  # Show first 200 chars
    
    # Remove SQL comments first
    sql_text = remove_sql_comments(sql_text)
    print(f"DEBUG - After comment removal: {repr(sql_text[:200])}...")
    
    # Clean and normalize the SQL
    sql_text = sql_text.replace(',', ' ')
    sql_text = sql_text.replace('(', ' ')
    sql_text = sql_text.replace(')', ' ')
    sql_text = sql_text.replace('\r', ' ')
    sql_text = sql_text.replace(';', ' ')
    sql_text = sql_text.replace('"', '')
    sql_text = re.sub(r'\bAS\b', ' ', sql_text, flags=re.IGNORECASE)
    
    # Split into words and remove empty strings
    words = [word.strip().upper() for word in sql_text.split() if word.strip()]
    print(f"DEBUG - Words after processing: {words[:20]}...")  # Show first 20 words
    
    obj_list = []
    
    # Find FROM and JOIN keywords
    from_positions = [i for i, word in enumerate(words) if word == 'FROM']
    join_positions = [i for i, word in enumerate(words) if word == 'JOIN']
    
    print(f"DEBUG - FROM positions: {from_positions}")
    print(f"DEBUG - JOIN positions: {join_positions}")
    
    # Extract table names after FROM
    for pos in from_positions:
        if pos + 1 < len(words):
            potential_table = words[pos + 1]
            print(f"DEBUG - Checking FROM table: '{potential_table}'")
            if re.match(r'^[A-Z0-9_-]+\.[A-Z0-9_-]+$', potential_table):
                print(f"DEBUG - Added FROM table: {potential_table}")
                obj_list.append(potential_table)
            else:
                print(f"DEBUG - FROM table didn't match pattern: {potential_table}")
    
    # Extract table names after JOIN
    for pos in join_positions:
        if pos + 1 < len(words):
            potential_table = words[pos + 1]
            print(f"DEBUG - Checking JOIN table: '{potential_table}'")
            if re.match(r'^[A-Z0-9_-]+\.[A-Z0-9_-]+$', potential_table):
                print(f"DEBUG - Added JOIN table: {potential_table}")
                obj_list.append(potential_table)
            else:
                print(f"DEBUG - JOIN table didn't match pattern: {potential_table}")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_obj_list = []
    for obj in obj_list:
        if obj not in seen:
            seen.add(obj)
            unique_obj_list.append(obj)
    
    print(f"DEBUG - Final result: {unique_obj_list}")
    return unique_obj_list

def check_table_or_view(obj,cur):
    x = obj.split(".")
    query = "SELECT TABLEKIND FROM DBC.TABLES WHERE DATABASENAME='{dbname}' AND TABLENAME='{objname}'".format(dbname=x[0],objname=x[1])
    output = cur.execute(query)
    comment = ""
    try:
        out = output.fetchall()[0][0].strip()
    except:
        comment = "not able to identify view or table"
        out = 'T'
    return out, comment
def view_analysis(view,cur):
    query = "show view {viewname}".format(viewname=view)
    print(query)
    try:          
        output = cur.execute(query)
        output = output.fetchall()
        src_list = get_object_names(output)
        print(src_list)
        lst = []
        if len(src_list):
            for src in src_list:
                obj_type,comment = check_table_or_view(src,cur)
                lst.append([view,src,obj_type,comment])
            return lst
        else:
            lst = [[view, "","","couldn't find the sources please do it manually"]]
            return lst
    except:
        lst = [[view, "","","does not exist"]]
        return lst
def views_analysis(input_list,cur):
    lst=input_list
    output=[]
    for ls in lst:
        output.extend(view_analysis(ls,cur))
    df = pd.DataFrame(output,columns=["VIEW", "SOURCE", "SOURCETYPE","COMMENT"])
    df1 = df[df["SOURCETYPE"]=='V'].SOURCE.unique()
    again_view_list= []
    for view in df1:
        if view not in df.VIEW.unique() and view!='':
            again_view_list.append(view)
    while(len(again_view_list)):
        for view in again_view_list:
            df = df._append(pd.DataFrame(view_analysis(view,cur),columns=["VIEW", "SOURCE", "SOURCETYPE","COMMENT"]))
        df1 = df[df["SOURCETYPE"]=='V'].SOURCE.unique()
        again_view_list= []
        for view in df1:
            if view not in df.VIEW.unique() and view!='':
                print(view, df.VIEW.unique())
                again_view_list.append(view)
    df.drop_duplicates()
    return df