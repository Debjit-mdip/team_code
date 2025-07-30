import pandas as pd
import re
import os
import connect_td_ssh as sh
import streamlit as st
import Find_Pks as fpk
import viewanalysis as va

def run_query(query,cur):
    print(query)

    r=[]
    try:          
        output = cur.execute(query)
        print(output)
        if len(r):
            r.extend(output.fetchall())
        else:
            r = output.fetchall() 
    
    except Exception as e:
        st.error(e)
        r=[]
    finally:
        return r

def tbl_information(table_nam_list,teradata_cursor):
    without_db,db_name_list,tbl_name_list = [],[],[]
    for x  in table_nam_list:
        try:
            db_name,tbl_name = x.split(".")
            db_name_list.append(db_name)
            tbl_name_list.append(tbl_name)
        except:
            without_db.append(x)

    db_name_set = tuple(set(db_name_list))
    tbl_name_set = tuple(set(tbl_name_list))
    # print(db_name_set,tbl_name_set)

    if len(db_name_set) ==1 and len(tbl_name_set) ==1:
        db_name = db_name_set[0]
        tbl_name = tbl_name_set[0]
        condition_db = f" = '{db_name}'"
        condition_tbl = f" = '{tbl_name}'"
    elif len(db_name_set) ==1:
        db_name = db_name_set[0]
        condition_db = f" = '{db_name}'"
        condition_tbl = f"IN {tbl_name_set}"
    else:
        condition_db = f"IN {db_name_set}"
        condition_tbl = f"IN {tbl_name_set}"


    query_size_ddl = f"""SELECT
     B.DatabaseName
    ,B.tablename
    ,B.Version
    ,B.TableKind 
    ,B.RequestText
    ,CreateTimeStamp
    ,CAST(SUM(CURRENTPERM) AS DECIMAL(38,5))/(1024*1024) AS TABLE_SIZE_MB
    ,CAST(SUM(CURRENTPERM) AS DECIMAL(38,5))/(1024*1024*1024) AS TABLE_SIZE_GB
FROM dbc.tablesize A
RIGHT JOIN DBC.TABLES B
	ON A.TABLENAME=B.TABLENAME
    AND A.DatabaseName = B.DatabaseName
    WHERE B.DatabaseName {condition_db}
    AND B.tablename {condition_tbl}
GROUP BY 1,2,3,4,5,6;
        """

    tbl_size_ddl_output = run_query(query_size_ddl,teradata_cursor)
    tbl_size_ddl_df_columns = ['DatabaseName','TableName','Version','Object Type','DDL','CreateTimeStamp','TABLE_SIZE_MB','TABLE_SIZE_GB']
    tbl_size_ddl_df = pd.DataFrame(tbl_size_ddl_output,columns=tbl_size_ddl_df_columns)
    # st.dataframe(tbl_size_ddl_df)
    tbl_size_ddl_df['Object Name'] = tbl_size_ddl_df['DatabaseName'].str.upper().str.strip() +"."+ tbl_size_ddl_df['TableName'].str.upper().str.strip()
    tbl_size_ddl_df.drop(['DatabaseName','TableName'],axis=1,inplace=True)
    tbl_size_ddl_df['Object Type'] = tbl_size_ddl_df['Object Type'].apply(lambda x: 'Table' if x.strip()=="T" else ('View' if x.strip()=="V" else ('Procedure' if x.strip() == 'P' else x.strip())))
    filtered_tbl_size_ddl_df = tbl_size_ddl_df[tbl_size_ddl_df['Object Name'].isin(table_nam_list)]
    # st.dataframe(filtered_tbl_size_ddl_df)

    #------------ update ddl where version>1 ----------
    version_df = filtered_tbl_size_ddl_df[filtered_tbl_size_ddl_df['Version'] > 1]
    Object_list = version_df['Object Name'].values.tolist()
    Object_type_list = version_df['Object Type'].values.tolist()
    lst =[]
    for idx,obj in enumerate(Object_list):
        query_ddl = f"show {Object_type_list[idx]} {obj}"
        # st.text(query_ddl)
        tbl_ddl_lst = run_query(query_ddl,teradata_cursor)
        lst.append([Object_list[idx],tbl_ddl_lst[0][0]])
    ddl_df = pd.DataFrame(lst,columns=['Object Name','DDL_new'])
    # st.dataframe(ddl_df)

    filtered_tbl_size_ddl_df = filtered_tbl_size_ddl_df.merge(ddl_df,on = "Object Name", how = "left")
    filtered_tbl_size_ddl_df.loc[filtered_tbl_size_ddl_df['Version'] > 1,'DDL'] = filtered_tbl_size_ddl_df.loc[filtered_tbl_size_ddl_df['Version'] > 1,'DDL_new']
    filtered_tbl_size_ddl_df.drop(columns=['DDL_new','Version','CreateTimeStamp'],inplace=True)
    
    

    
    #----------- count ------------
    output_count_list = []
    total = len(table_nam_list)
    progress_bar = st.progress(0)
    status_text = st.empty()
    status_placeholder = st.empty()
    updt_column_lst = ['dw_last_updt_dtm','dw_updt_dtm','dw_updt_dte']
    for i,table_name in enumerate(table_nam_list,start=1):
        table_ddl = filtered_tbl_size_ddl_df.loc[filtered_tbl_size_ddl_df['Object Name'] == table_name, 'DDL'].values
        # updt_column = fpk.extract_updt_column(table_name, table_ddl, updt_column_lst)


        query_count = f"""select '{table_name}' as Tablename, cast(count(*) as bigint) as table_count from {table_name}; """
        query_delta_count = f"""select '{table_name}' as Tablename, cast(count(*) as bigint) as table_count from {table_name}; """
        try:
            output = run_query(query_count,teradata_cursor)
        except Exception as e:
            na_e = f"NA ({e})"
            output = [[table_name,na_e]]  # add not found/NA
        output_count_list.extend(output)

        progress = int((i/total))*100
        progress_bar.progress(progress)
        status_text.text(f"Running query {i} of {total}... ")
        # print(f'remaining: {l-i-1}')

    tbl_count_df_columns = ['Object Name','Count']
    tbl_count_df = pd.DataFrame(output_count_list,columns=tbl_count_df_columns)

    #------------------ merge count and ddl df ----------------------
    merged_info_df = pd.merge(tbl_count_df,filtered_tbl_size_ddl_df,on = "Object Name", how = "left")

    tbl_ddls_list = fpk.extract_pks_from_bteqs(merged_info_df[['Object Name','DDL']])
    tbl_ddls_df = pd.DataFrame(tbl_ddls_list, columns=['Object Name','Primary Key'])
    merged_info_pk_df =  pd.merge(merged_info_df,tbl_ddls_df, on = 'Object Name',how='inner')
    return merged_info_pk_df

def table_size_ddl(table_nam_list, environment='qa', username=None, password=None, progress_callback=None, status_callback=None):
    teradata_connection = sh.connect_teradata(environment=environment, username=username, password=password)
    teradata_cursor = teradata_connection.cursor()
    st.text("Running Teradata Queries...")
    table_nam_list = [item.upper() for item in table_nam_list]

    merged_info_pk_df1 = tbl_information(table_nam_list,teradata_cursor)

    
    #----------- update df where type - View ---------
    view_df = merged_info_pk_df1[merged_info_pk_df1['Object Type'] =='View']
    # st.dataframe(view_df)
    Object_list = view_df['Object Name'].values.tolist()
    Object_view_list = list(set(Object_list))
    view_out_df = va.views_analysis(Object_view_list,teradata_cursor)
    st.dataframe(view_out_df)
    obj_list1 = view_out_df['VIEW'].str.upper().tolist()
    obj_list2 = view_out_df['SOURCE'].str.upper().tolist()
    obj_list = obj_list1 + obj_list2
    obj_list_set = list(set(obj_list))

    filtered_obj_list = [obj for obj in obj_list_set if obj not in table_nam_list]

    if(len(filtered_obj_list))>0:
        merged_info_pk_df2 = tbl_information(filtered_obj_list,teradata_cursor)
        # st.dataframe(merged_info_pk_df1)
        # st.dataframe(merged_info_pk_df2)

        merged_info_pk_df =  pd.concat([merged_info_pk_df1,merged_info_pk_df2], ignore_index=True)
    else:
        merged_info_pk_df = merged_info_pk_df1


    #------------- teradata connection close ---------------
    try:
        teradata_connection.close()
        st.success("Teradata connection closed!")
    except Exception as e:
        st.error(e)

    return(merged_info_pk_df)

    



