import fabric
import re
import pandas as pd
import ExcelToList
import connect_td_ssh as sh
import APP_ENV as env


def save_file(output_file_path,dff):
    writer = pd.ExcelWriter(output_file_path, engine='xlsxwriter') 
    dff.to_excel(writer, sheet_name='Sheet1', index=False)
    writer._save()

def run(command,c,table_nm,Layer,database=''):
    _,cd,_,cmd=command.split("&&")
    print(f'{cd.strip()}\n{cmd.strip()}')
    out=str(c.run(command,hide=False,warn=True))

    if Layer.upper()=='ACQ':
        stgdb = '${PRJ_STG_DB}'
        stgMatch=re.compile(r"(.*?):\s*.+ "+stgdb+r"\."+table_nm+r"_stg\s",re.IGNORECASE).findall(out)
        tblmatch=re.compile(r"(.*?):\s*(?:INSERT|UPDATE|MERGE|DELETE).+"+database+'.+'+table_nm+r'\s',re.IGNORECASE).findall(out)
        clnMatch=re.compile(r"(.*?):\s*INSERT.+"+database+'.+'+table_nm+"_stg_cln"+'\s',re.IGNORECASE).findall(out)
        TPTmatch=re.compile(r"(.*?\w+.tpt):DEFINE JOB\s*"+table_nm+"_stg_UPLOAD",re.IGNORECASE).findall(out)
        # output=list(set(insMatch+updMatch+merMatch+insMatch1+insMatch2))
        output=list(set(tblmatch+clnMatch+stgMatch+TPTmatch))
    else:
        # out=re.compile(rf"^(?!.*BKP_)(?!.*\d+\.\w+).*{database}.{table_nm}*", re.IGNORECASE | re.MULTILINE).findall(out)

        insMatch1=re.compile(r"(.*?):\s*INSERT.+"+database+'.+'+table_nm+'\s',re.IGNORECASE).findall(out)
        insMatch2=re.compile(r"(.*?):\s*INSERT.+"+database+'.+'+table_nm+"_stg"+'\s',re.IGNORECASE).findall(out)
        insMatch3=re.compile(r"(.*?):\s*INSERT.+"+database+'.+'+table_nm+"_stg_cln"+'\s',re.IGNORECASE).findall(out)
        updMatch=re.compile(r"(.*?):\s*UPDATE.+"+database+'.+'+table_nm+'\s',re.IGNORECASE).findall(out)
        merMatch=re.compile(r"(.*?):\s*MERGE.+"+database+'.+'+table_nm+'\s',re.IGNORECASE).findall(out)
        CreateMatch=re.compile(r"(.*?):\s*CREATE.+"+database+'.+'+table_nm+'\s',re.IGNORECASE).findall(out)
        DeleteMatch=re.compile(r"(.*?):\s*DELETE.+"+database+'.+'+table_nm+"_stg"+'\s',re.IGNORECASE).findall(out)
        TPTmatch=re.compile(r"(.*?\w+.tpt):DEFINE JOB\s*"+table_nm+"_stg_UPLOAD",re.IGNORECASE).findall(out)
        # output=list(set(insMatch+updMatch+merMatch+insMatch1+insMatch2))
        output=list(set(insMatch1+insMatch2+insMatch3+updMatch+merMatch+CreateMatch+DeleteMatch+TPTmatch))
    return output

def RE(table,Layer,dic,ssh,path):
    table_nm = table.split('.',1)[1]
    if Layer.upper()=='ACQ':
        folders = ["master", "sales", "operations", "fin", "surrkey", "trade", "um", "mkt", "social"]
        final_output=[]
        for folder in folders:
            command=f"pwd && cd {path}{folder}/bin/loader && pwd && grep -iwE '{table_nm}|{table_nm}_STG_CLN|{table_nm}_STG' *.btq *.tpt"
            # print(command)
            output = run(command,ssh,table_nm,Layer)
            final_output = [f"{folder}/bin/loader/{x}" for x in output]
            if len(final_output):
                print(f"output: {final_output}\n")
                return final_output
    
    elif Layer.upper()=='DWL':
        try:
            database=dic[table.split('.')[0]]
        except:
            database = table.split('.')[0]
        command=f"pwd && cd {path} && pwd && grep -iw {table_nm} *.btq"
        print(command)
        final_output = run(command,ssh,table_nm,Layer,database)
        print(final_output)
    
    elif Layer.upper()=='APP':
        try:
            database=dic[table.split('.')[0]]
        except:
            database = table.split('.')[0]
        command=f"pwd && cd {path} && pwd && grep -iw {table_nm} *.*"
        print(command)
        final_output = run(command,ssh,table_nm,Layer,database)
        print(final_output)

    if not final_output:
        final_output = ['Not found']
        print("Not found\n")
    return final_output

def reveng(excel_object, path, Layer, hostname, port, username, password,uploaded_env_file):
    
    try:
        tables=ExcelToList.exceltolist(excel_object)
    except: 
        tables = excel_object

    dic={'DWL_P_INTL':'PRJ_INTL_DB',
        'DWL_P_DRVD':'PRJ_DRVD_DB',
        'FPS_P':'PRJ_FPS_DB',
        'ACQ_P':'PRJ_CORE_DB',
        'ACQ_P_SP':'PRJ_SP_DB',
        'ACQ_P_DIM':'PRJ_ACQ_DB',
        'ACQ_P_CORE':'PRJ_ACQ_CORE',
        'DWL_P_DATA':'PRJ_DATA_DB',
        'MDM_P_PUB':'PRJ_MDM_DB',
        'FLSDW_P':'PRJ_FLSDW_DB',
        'MDM_P':'PRJ_MDM_CORE',
        'MDM_P_SRC':'PRJ_MDM_SRC',
        'MDM_P_MST':'PRJ_MDM_MST',
        'DWL_P':'PRJ_VIEW_DB',
        'DWL_P_FLNA':'PRJ_FLNA_DB',
        'DWL_P_FLNA':'PRJ_FLNA_DB',
        'CAS_TPM_P':'PRJ_CAS_VIEW_DB',
        'POS_P':'PRJ_POS_DB',
        'LMDM_P':'LMDM_DB',
        'DWL_P':'PRJ_DWL_DB',
        'FL_P':'PRJ_FL_DB',
        'STAR2_P':'STAR2_DB',
        'STAR2_P_DATA':'STAR2_DATA_DB',
        'STAR2_P_NAB':'STAR2_NAB_DB',
        'PBC_P':'PBC_DB',
        'POS_P':'POS_DB',
        'DWL_P_PBNA':'PRJ_PBNA_DB',
        'PBDW_P':'PRJ_PBDW_DB',
        'PBDW_P_SCR':'PRJ_PBDW_SCR_DB',
        'FLNA_APP_P':'PRJ_FLNA_APP_DB',
        'PMF_P_FACTS':'PRJ_PMF_FACTS_DB',
        'PMF_P':'PRJ_PMF_VIEW_DB',
        'QTG_P2_BASE':'PRJ_QTG_BASE_DB',
        'QTG_P2':'PRJ_QTG_DB',
        'SSR_P':'SSR_DB',
        'SSR_P_FACTS':'PRJ_FACTS_DB',
        'ACQ_P_PBC':'PRJ_CORE_PBC_DB',
        'DWL_P_PBC ':'PRJ_DWL_PBC_DB',
        'QTG_SCX_P_BASE':'PRJ_QTG_SCX_DB',
        'DWL_P_BASE':'PRJ_BASE_DB',
        'BPL_P':'BPL_DB',
        'SUS_P':'SUS_DB',
        'PROD':'DWL_ENV',
        'DWL_P_RSTR':'PRJ_RSTR_DB',
        'DWL_P_RSTR_DATA':'PRJ_RSTR_DATA_DB',
        'ACQ_P_SEC':'PRJ_SEC_DB',
        'LATAM_BEV_P_DATA':'PRJ_LAB_DB',
        'LATAM_BEV_P':'PRJ_LAB_VIEW_DB',
        'AMENA_BSR_P_DATA':'AMENA_BSR_P_DATA',
        '':''}
    if Layer.lower() == 'app':
        dic = env.read_env_file(uploaded_env_file,dic)
        
    dff=pd.DataFrame({'Table_name':[], 'bteqs':[]})
    l=len(tables)
    print(f'total obj: {l}')

    # Create SSH connection using passed parameters
    ssh = fabric.Connection(
        host=hostname,
        port=port,
        user=username,
        connect_kwargs={'password': password}
    )
    for table in tables:
        btqs=RE(table,Layer,dic,ssh,path)
        df = pd.DataFrame({'Table_name': table, 'bteqs': btqs})
        dff=pd.concat([dff,df],axis=0)
        l-=1
        print(f'remaining: {l}')
        
    ssh.close()
    return dff 
    # save_file(output_file,dff)
