import os
import re
import sys
import pandas as pd
from ExcelToList import exceltolist
import APP_ENV as env

uploaded_env_file = ''
def read_env(layer):
    ENV_VAR = {'DWL':{'${PRJ_WORK_DB}':'DWL_P_INTL_WORK',
    '${PRJ_INTL_DB}':'DWL_P_INTL',
    '${PRJ_DRVD_DB}':'DWL_P_DRVD',
    '${PRJ_DRVD_WORK_DB}':'DWL_P_DRVD_WORK',
    '${PRJ_DRVD_JOB_DB}':'DWL_P_DRVD_JOB',
    '${PRJ_JOB_DB}':'DWL_P_INTL_JOB',
    '${PRJ_FPS_DB}':'FPS_P',
    '${PRJ_CORE_DB}':'ACQ_P',
    '${PRJ_SP_DB}':'ACQ_P_SP',
    '${PRJ_ACQ_DB}':'ACQ_P_DIM',
    '${PRJ_ACQ_CORE}':'ACQ_P_CORE',
    '${PRJ_DATA_DB}':'DWL_P_DATA',
    '${PRJ_MDM_DB}':'MDM_P_PUB',
    '${PRJ_FLSDW_DB}':'FLSDW_P',
    '${PRJ_MDM_CORE}':'MDM_P',
    '${PRJ_MDM_SRC}':'MDM_P_SRC',
    '${PRJ_MDM_MST}':'MDM_P_MST',
    '${PRJ_VIEW_DB}':'DWL_P',
    '${ERR_ARCHIVE_DAYS}':'30',
    '${PRJ_FLNA_DB}':'DWL_P_FLNA',
    '${PRJ_FLNA_WORK_DB}':'DWL_P_FLNA_WORK',
    '${PRJ_CAS_VIEW_DB}':'CAS_TPM_P',
    '${PRJ_POS_DB}':'POS_P',
    '${LMDM_DB}':'LMDM_P',
    '${PRJ_DWL_DB}':'DWL_P',
    '${PRJ_FL_DB}':'FL_P',
    '${STAR2_DB}':'STAR2_P',
    '${STAR2_DATA_DB}':'STAR2_P_DATA',
    '${STAR2_NAB_DB}':'STAR2_P_NAB',
    '${PBC_DB}':'PBC_P',
    '${POS_DB}':'POS_P',
    '${PRJ_PBNA_WORK_DB}':'DWL_P_PBNA_WORK',
    '${PRJ_PBNA_DB}':'DWL_P_PBNA',
    '${PRJ_PBDW_DB}':'PBDW_P',
    '${PRJ_PBDW_SCR_DB}':'PBDW_P_SCR',
    '${PRJ_FLNA_APP_DB}':'FLNA_APP_P',
    '${PRJ_PMF_FACTS_DB}':'PMF_P_FACTS',
    '${PRJ_PMF_VIEW_DB}':'PMF_P',
    '${PRJ_QTG_BASE_DB}':'QTG_P2_BASE',
    '${PRJ_QTG_DB}':'QTG_P2',
    '${SSR_DB}':'SSR_P',
    '${PRJ_FACTS_DB}':'SSR_P_FACTS',
    '${PRJ_CORE_PBC_DB}':'ACQ_P_PBC',
    '${PRJ_DWL_PBC_DB}':'DWL_P_PBC ',
    '${PRJ_QTG_SCX_DB}':'QTG_SCX_P_BASE',
    '${PRJ_BASE_DB}':'DWL_P_BASE',
    '${PRJ_BASE_WORK_DB}':'DWL_P_BASE_WORK',
    '${BPL_DB}':'BPL_P',
    '${SUS_DB}':'SUS_P',
    '${SUS_MSTR_DB}':' SUS_P_MSTR',
    '${PRJ_RSTR_WORK_DB}':'DWL_P_RSTR_WORK',
    '${PRJ_RSTR_DB}':'DWL_P_RSTR',
    '${PRJ_RSTR_DATA_DB}':'DWL_P_RSTR_DATA',
    '${PRJ_SEC_DB}':'ACQ_P_SEC',
    '${PRJ_LAB_DB}':'LATAM_BEV_P_DATA',
    '${PRJ_LAB_VIEW_DB}':'LATAM_BEV_P',
    '${PRJ_EUFIN_DB}':'EUFIN_P_DATA',
    '${DLAB_DB}':'DLAB_PBC',
    '${TGT_DB}':'pgt_flna_ibp_P',
    '${PEPCMN_ENV}':'PEPCMN_PRD',
    '${PEPCMN_DB}':'PEPCMN_P',
    '${PEPCMN_DATA}':'PEPCMN_P_DATA',
    '${FL_DB}':'FL_P',
    '${ACQ_DB}':'ACQ_P',
    '${MDM_DB}':'MDM_P',
    '${DWL_DB}':'DWL_P',
    '${AMESAAPAC_DB}':'AMESAAPAC_P',
    '${AMESAAPAC_DB_DATA}':'AMESAAPAC_P_DATA',
    '${PMM_DB}':'PMM_P',
    '${AMENA_CMRCL_DB}':'AMENA_CMRCL_P',
    '${APAC_GTM_DB}':'APAC_GTM_P',
    '${PEPCMN_DB}':'PEPCMN_P',
    '${AMENA_FIN_DB}':'AMENA_FIN',
    '${AMESAAPAC_DB_WORK}':'AMESAAPAC_P_WORK',
    '${PRJ_POR}':'AMENA_FIN',
    '${PRJ_ACQ}':'ACQ_P',
    '${PRJ_DWL}':'DWL_P',
    '${AMENA_LAB}':'DLAB_AMENA'},
    'ACQ': {'${PRJ_WORK_DB}':'ACQ_P_WORK',
    '${PRJ_UTIL_DB}':'ACQ_P_UTIL',
    '${PRJ_JOB_DB}':'ACQ_P_JOB',
    '${PRJ_STG_DB}':'ACQ_P_STAGE',
    '${PRJ_CORE_DB}':'ACQ_P_CORE',
    '${PRJ_MDM_DB}':'MDM_P',
    '${PRJ_DIM_DB}':'ACQ_P_DIM',
    '${PCU_DB}':'PCU_P',
    '${PRJ_DIM}':'ACQ_P',
    '${PRJ_DB}':'ACQ_P',
    '${PRJ_SP_DB}':'ACQ_P_SP',
    '${PRJ_ACQ_PSTG_DB}':'ACQ_P_PSTG_UTIL',
    '${PEPCMN_ENV}':'PEPCMN_PRD',
    '${PEPCMN_DB}':'PEPCMN_P',
    '${PEPCMN_DATA}':'PEPCMN_P_DATA',
    '${FL_DB}':'FL_P'},
        'APP':{}
    }
    if layer.lower() == 'app':
        ENV_VAR = env.read_env_file(uploaded_env_file,ENV_VAR)
    return ENV_VAR

database_list = ['SEM_GTM_FLNA', 'PEDW_P_STAR2_WORK', 'PBDW_P_SAM_JOB', 'SEM_PBF', 'FLSDW_LGL_DATA', 'QTG_P2_BASE', 'DLAB_EUSLS', 'SEM_CAS_TPM', 'SEM_FDS', 'IFOD_P_STAGE', 'PMF_P_FACTS', 'PBDW_P_SCR', 'PBDW_P_DSHB_DATA', 'SEM_MDM', 'PDCRTPCD', 'FPS_P_UTIL', 'PQP_P_DATA', 'QTG_P2_STG', 'PBDW_P_PPM', 'ECOMM_P_DATA', 'SEM_PMM', 'PBDW_P_MAA', 'ACQ_P_UM_DATA', 'MDM_P_CRDM', 'FLSDW_P_FLR', 'PBDW_P_DFR_STAGE', 'SEM_EUSCA', 'DLAB_AMENA', 'CAS_TPM_P_UTIL', 'DLAB_QFNA', 'STAR2_P_FY2009', 'GSC_P_UTIL', 'PBDW_P_SFSO', 'AMENA_ANZ_P_DATA', 'IPHONE_P_JOB', 'PEDW_P_STAR2_EXT', 'AMESA_MVS_P', 'PGT_FLNA_IBP_P', 'PBDW_P_PMAX', 'PBDW_P_BOSTFS_DATA', 'PBDW_P_SS_JOB', 'PBDW_P_DBA', 'SEM_NASS', 'PBF_P_STAGE', 'SEM_AAS', 'CAS_FM_P_FACTS', 'querygrid', 'PGRE_SPC_MGMT_P', 'PBDW_P_CRT_STAGE', 'DLAB_PBDW', 'SEM_LATAM_BEV', 'EUFIN_P', 'SEM_CKPI', 'RECOVER', 'BPL_P_DATA', 'PEDW_P_STAR2_ACNTR', 'STAR2_P_RBS_DATA', 'SEM_PBDW_SNC', 'AMESAAPAC_P_DATA', 'AMESA_RPRTNG_P', 'ACQ_P_SEC', 'QTG_SCX_P2_STG', 'PEDW_P_STAR2_EXT_STAGE', 'SEM_LAT_RM', 'voltage', 'DBC', 'COMGS_P', 'TKEDW_P', 'FLSDW_P_WORK', 'PEDW_P_STAR2_EXT_WORK', 'SEM_EDA', 'AMESAAPAC_P_WORK', 'CAO_P_STAGE', 'CAO_P_JOB', 'CAS_TPM_P_WORK', 'DWL_P_DRVD_JOB', 'APAC_GTM_P_WORK', 'QTG_SCX_P2_VW', 'QTG_P2_VW', 'PEDW_P_STAR2_STAGE_STAR20', 'SEM_FLW_LGL', 'SEM_PBDW_MAA', 'CPPTSTG', 'AMENA_CMRCL_P', 'NAB_APP_P', 'SEM_NAB_DIGDASH', 'PEDW_P_STAR2_GEO', 'FL_P_MSTR', 'SEM_APAC_GTM', 'console', 'FL_P', 'PEDW_P_STAR2_SCTY_VW', 'PBDW_P_IPSCR', 'DLAB_BIERT', 'TDStats', 'DWL_P_DRVD_WORK', 'PBDW_P_SS_WORK', 'POS_P_UTIL', 'TDMaps', 'PBDW_P_DEAL', 'ACQ_P_CORE', 'STAR2_XP_DATA', 'PBDW_P_BOPNR', 'DWL_P', 'ACQ_P_SEC_DATA_UM', 'PBDW_P_INTG_DATA', '9367608', 'CAO_P_DATA', 'SEM_TKEDW', 'BPL_P_STAGE', 'LATAM_BEV_P_WORK', 'TPMA_DATA', 'DWL_P_PBNA', 'SEM_PFC_TPM', 'STAR2_P_SCTY', 'Crashdumps', 'BPL_P_WORK', 'QTG_SCX_P2_BASE', 'AMENA_CMRCL_P_DATA', 'DLAB_STAR', 'SEM_RTM', 'LATAM_BEV_P_DATA', 'SEM_ACLD', 'FL_P_SP', 'PDCRAdmin', 'SEM_POR', 'qcd', 'PBDW_P_CIV_DATA', 'LMDM_P_WORK', 'DLAB_WALMART', 'TPMA', 'NRM_P', 'SCP_BEV_P_DATA', 'vormetric', 'DLAB_CNTRL', 'AMENA_CMRCL_P_WORK', 'SEM_TE', 'IFOD_P_UTIL', 'CPPTDATA', 'tdviewpoint', 'SEM_PGRE_SPC_MGMT', 'SLSTALRT_P_SP', 'DWL_P_RSTR_DATA', 'SLSTALRT_P_JOB', '9376770', 'TD_SYSFNLIB', 'STAR2_P_PNB_DATA', 'FLSDW_P_DATA', 'ODW_P_DATA', 'SEM_DSLD', 'EDW_MDM_P', 'NASS_TE_P_DATA', 'DLAB_CAO_POC', 'SEM_AMENA_FIN', 'PBDW_P_PTS', 'SEM_GLBL_COM', 'SEM_FLNA', 'GCA_P', 'GEOSC_P_DATA', 'ACQ_P_SEC_CORE', 'MDM_P_MST', 'PBDW_P_RTM_STAGE', 'APAC_OPEX_P', 'LMDM_P_NC', 'PBDW_P_IP', 'MDM_P_UCBKUP', 'EXTRCT_P_WORK', 'SEM_NAB', 'SysDBA', 'SEM_NRM', 'EDA_P', 'SLSTALRT_P_STAGE', 'PBDW_P_SCR_DATA', 'DLAB_CI', 'PEDW_P_STAR2_CAL', 'PBDW_P_IPSCR_DATA', 'DWL_P_DATA', 'PAID_P', 'SLSTALRT_P_UTIL', 'PBDW_P_INTG_STAGE', 'CAS_TPM_P', 'PDCRINFO', 'PBDW_P_INTG_JOB', 'MDM_P_PUB', 'DLAB_WASTE', 'SEM_CCAT', 'STAR2_P_AUX1', 'FOD_P', 'STAR2_P_FY2011', 'PAID_P_WORK', 'ISCP_P_JOB', 'DWL_P_FLNA_WORK', 'DWL_P_ETL', 'PBF_P_UTIL', 'PEDW_P_WORK', 'dbcmngr', 'PMDM_PRESTAGE_P', 'PEDW_P_STAR2_UTIL', 'CAO_P', 'EUSCA_P_WORK', 'QTG_SCX_P2_UTIL', 'LMDM_P', 'SUS_P_STG', 'DB_Sandbox_Admin', 'LMDM_P_OUT', 'AMENA_ANZ_P_STAGE', 'DWL_P_SP', 'SEM_PQP', 'STAR2_P_DATA', 'PBDW_P_SFA', 'PTE_P', 'GLBL_FIN_P', 'FLSDW_P_JOB', 'SEM_AMENA_ANZ', 'SystemFe', 'SEM_PQP_VLDTN', 'DLAB_SFSX', 'EUSCA_P_DATA', 'PAID_P_MATV', 'NRM_P_DATA', 'STAR2_P_NAB', 'PBDW_P_SS', 'PMM_P_WORK', 'SEM_GCA', 'ISCP_P_WORK', 'PBDW_P_DBA_WORK', 'PEDW_P_HIER', 'APAC_OPEX_P_DATA', 'PBDW_P_HRZN_DATA', 'PBDW_P_DBA_JOB', 'FL_P_CPY', 'FOD_P_DATA', 'CAO_P_WORK', 'PBDW_P_PTS_DATA', 'PEDW_P_STAR2_TRSPN', 'NASS_TE_P_JOB', 'AMESA_MVS_P_WORK', 'TPO_WM_P_DATA', '9338835', 'dbcmngr6', 'DWL_P_INTL', 'SEM_WASTE', 'QTG_SCX_P2_JOB', 'ACQ_P_UM', 'STAR2_P_JOB', 'RUSDA_P', 'PBDW_P_COMMON', 'VBN_P_DDW', 'QTG_SCX_P2', 'VBN_P_CDW', 'PFC_TPM_P_STAGE', 'DLAB_CIO', 'RUSDA_P_STAGE', 'ACQ_P_PBC_UTIL', 'PBDW_P_PPM_JOB', 'CAS_TPM_P_STAGE', 'demouser', 'PBDW_P_PMAX_DATA', 'CKPI_P_WORK', 'MDM_P_WORK', 'PEDW_P_STAR2_PRMTN', 'TDQCD', '9335928', 'LATAM_BEV_P_JOB', 'DLAB_SFI', 'PBDW_P_DFR', 'STAR2_P_FY2009_DATA', 'DLAB_SIG', 'MDW_P_QLTY', 'ISCP_P', 'SLSTALRT_P_DATA', 'PEPCMN_P', 'MDM_P_TIPS', 'CAO_P_SP', 'VBN_P_EDR', 'SEM_AMENA_BSR', 'COMGS_P_DATA', 'STAR2_P_FY2017_DATA', 'ACQ_P_DIM', 'GCA_P_JOB', 'ACQ_P_ULOAD', 'AMESA_RM_P', 'CNSMR_INSGHT_P_DATA', 'PBDW_P_INTG', 'PFC_TPM_P_WORK', 'PBDW_P_BOSTFS', 'ACQ_P_SP', 'PDCRDATA', 'STAR2_P_FY2013_14_15', 'NASS_AP_P', 'PMM_P', 'POS_P', 'SEM_PBDW_CETS', 'MDW_P_JOB', 'STAR2_P_FY2008_DATA', 'SEM_PBDW_PNB', 'PBDW_P_IPSLT', 'MDW_P', 'PBDW_P_RPTNG_DATA', 'TPumpMacro', 'FPS_P_FACTS', 'LMDM_P_VER', 'PEDW_P_STAR2_TX', 'PEDW_P_STAR2_TAX', 'PDCRSTG', 'CAT_P_DATA', 'SYSBAR', 'PAID_P_BASE', 'MDM_IS_P', 'STAR2_P_RBS', 'SYSSPATIAL', 'IIE_P', 'PBDW_P_PTA_JOB', 'SEM_AMENA_CMRCL', 'PBDW_P_DSH', 'PBDW_P_WHSS', 'EUFIN_P_WORK', 'PEDW_P_QTG1', 'IPHONE_P_DATA', 'CAT_P', 'PBDW_P_IPS_DATA', 'DLAB_PMF', 'SEM_DMS', 'TKEDW_P_WORK', 'POS_P_JOB', 'PEDW_P_STAR2_LOC', 'PEDW_P_STAR2_ITEM', 'GDQ_P_WORK', 'IDF_WM_P_DATA', 'RSRSCH_RPTR_P_DATA', 'CFR_P_STAGE', 'APAC_OPEX_P_STAGE', 'GSC_P', 'TEMP_BKP', 'STAR2_P_PNB', 'PFC_TPM_P_UTIL', 'DLAB_TE', 'PEDW_P_STAR2_GL', 'SEM_GLBL', 'ACQ_P_PBC', 'SSR_P', 'CAT_P_JOB', 'SEM_SELLIN', 'ECI_XP_STAR2', 'GDQ_P', 'PBDW_P_TABSC', 'PBDW_P_ACL', 'AMESAAPAC_P', 'AMENA_BSR_P', 'PBDW_P_DFR_DATA', 'SLST_P', 'SEM_AMESA_PKNS', 'LockLogShredder', 'AMENA_ANZ_P', 'PAID_P_DW', 'GSC_P_DATA', 'PBDW_P_INP', 'SEM_QIS_FLNA', 'STAR2_P_CDA_SF', 'DLAB_EUCTS', 'SLST_P_DATA', 'DLAB_ECOMM', 'IIE_P_JOB', 'DBAWORK', 'SYSJDBC', 'PEDW_P_STAR2_PRTY', 'DLAB_DScube_P', 'APAC_GTM_P_DATA', 'CAS_TPM_P_FACTS', 'POS_P_STAGE', 'SEM_PBDW_BOST', 'SEM_SFOD', 'SSR_P_WORK', 'PBDW_P_BOST', 'STAR2_P_CDA_WORK', 'DLAB_BI4_TRAIN', 'SMARTR_P', 'PBDW_P_IPS', 'PBDW_P_SKI', 'PBDW_P_SAM_DATA', 'SEM_PBDW_BOSTFS', 'GEOSC_P', 'GCA_P_WORK', 'FLSDW_EXTRACT_UTIL', 'COMGS_P_WORK', 'CKPI_P_STAGE', 'SEM_STSRVY', 'DLAB_REPANA', 'STAR2_P_NAB_DATA', 'PBDW_P_CPS', 'PBDW_P_DEAL_STAGE', 'GLBL_FIN_P_DATA', 'STAR2_P_FY2006_DATA', 'SEM_EUFIN', 'RUCWD_P_DATA', 'DLAB_ESSBASE', 'QTG_P2_JOB', 'DWL_P_BASE_WORK', 'EDA_P_UTIL', 'STAR2_P_SP', 'NASS_TE_P', 'FLSDW_P_SP', 'EDA_P_DATA', 'PDCRDATA_HST', 'POS_P_WORK', 'DMS_P_WORK', 'IPRO_P_WORK', 'PBDW_P_CRT', 'FLSDW_P_STAGE', 'DLAB_GP', 'POS_P_CORE', 'STAR2_P_FY2008', 'BPM_P', 'EDA_P_WORK', 'PEDW_P_STAR2_DELTA', 'ACLD_P', 'DWL_P_PBNA_WORK', 'PBDW_P_LTTS', 'PBDW_P_SFA_DATA', 'PBDW_P_HRZN_STAGE', 'AMESA_MVS_P_DATA', 'IDF_WM_P_MINP', 'QTG_P2_BASE_HIST', 'STAR2_P_WORK', 'CFR_P_DATA', 'PEDW_P_STAR2_HIER', 'SEM_FPS', 'PBDW_P_RTM', 'ODW_P_STAGE', 'IPRO_P', 'SEM_PMF', 'APAC_GTM_P', 'LRM_P', 'DWL_P_FLNA', 'SEN_P', 'SEM_AMENA_GTM', 'DWL_P_BASE', 'IFOD_P', 'SEM_GLBL_PRCRMT', 'MDM_P_NC', 'SEM_COMGS', 'SQLJ', 'SEM_EHANA_SAP', 'AMENA_FIN_DATA', 'PEDW_P_STAR2_HR', 'ACQ_P_STAGE', 'PBDW_P_IPRO', 'PEPCMN_P_DATA', 'AMENA_GTM_P', 'PBDW_P', 'SEM_AMESA_RPRTNG', 'POR_P_WORK', 'PBDW_P_RTM_DATA', 'tdprodviewpoint', 'SEM_CAS_FM', 'DWL_P_RSTR_WORK', 'AMENA_ANZ_P_WORK', 'FLSDW_LGL', 'RECHDY76G', 'PBDW_P_KPI', 'RUSDA_P_DATA', 'PERFANALYSIS', 'MDM_P_HM', 'AMESA_RPRTNG_P_DATA', 'SEM_ERT', 'SEM_BPM', '9292499', 'SEM_GLBL_PRDTVTY', 'SEN_P_WORK', '9337216', 'SUS_P_WORK', 'POR_P_DATA', 'FL_P_JOB', 'AMENA_BSR_P_DATA', 'EDWDECODED', 'STAR2_P_FY2006', 'GSC_P_SP', 'IDF_WM_P', 'ACQ_P_UTIL', 'SEM_EXTRCT', 'PBDW_P_RPTNG_STAGE', 'TPO_WM_P', 'EDA_P_STAGE', 'MDM_P_VER', 'PBDW_P_MAA_UTIL', 'FL_P_UTIL', 'FPS_P', 'AMESA_RPRTNG_P_JOB', 'TKEDW_P_DATA', 'TAIWAN_P', 'PBDW_P_SAM', 'SEM_ABA', 'FPS_P_STAGE', 'ACQ_P_HIST', 'MDM_P_REP', 'PTE_P_DATA', 'DLAB_Xcelerator', 'IIE_P_DATA', 'LMDM_P_MST', 'PBDW_P_MAA_STAGE', 'PEDW_P_QTG1_CAL', 'STAR2_P_CDA', 'QTG_DLX_BASE', 'DLAB_SECE', 'PBDW_P_CRT_DATA', 'PFC_TPM_P_SP', 'PBDW_P_HRZN', 'STAR2_P_FY2017', 'AMENA_FIN', 'BPL_P', 'QTG_P2_UTIL', 'SUS_P_MSTR', 'SEM_SSR', 'SEM_FLW', 'PBDW_P_PMX', 'PBDW_P_WHP', 'SEM_ISCP', 'STAR2_P_FY2010', 'PBDW_P_EDR', 'PKNS_P_STAGE', 'GLBL_COM_P_DATA', 'SEN_P_DATA', 'PBDW_P_BOST_DATA', 'MDM_P_OUT', 'NASS_AP_P_DATA', 'FLSDW_LGL_MASTR', 'ECI_XP_SDW', 'DWL_P_INTL_WORK', 'CFR_P', 'BIM_REPOSITORY', 'MDM_P_SRC', 'TD_SYSXML', 'MDM_REFRESH_BKP', 'STAR2_P_FY2011_DATA', 'FL_P_STAGE', 'DLAB_QTGKPI', 'DSC_P_WORK', 'STAR2_P_FY2010_DATA', 'MDM_P_PROV', 'QTG_P2_SP', 'QTG_P2_MATV', 'SEM_INSGHT', 'DWL_P_INTL_JOB', 'PBDW_P_FSV', 'TD_SERVER_DB', 'CNSMR_INSGHT_P_STAGE', 'DWL_P_DRVD', 'STAR2_P_FY2012_DATA', 'SEM_EUIBP', 'PBF_P_JOB', 'PBDW_P_DSH_DATA', 'CANARY_SEM_STSRVY_P', 'FLNA_APP_P', 'ACQ_P_MINP', 'PBDW_P_EDOT', 'FL_P_WORK', 'LMDM_P_IN', 'PBDW_P_PSC_DATA', 'SSR_P_FACTS', 'GSC_P_STAGE', 'PBDW_P_DSHCCO_DATA', 'SEM_BPL', 'DWL_P_PBC', 'SEM_IPRO', 'SSR_P_MSTR', 'PGRE_SPC_MGMT_P_DATA', 'PBDW_P_IP_STAGE', 'ACQ_P_HR', 'PBDW_P_PTA', 'IPHONE_P', 'STAR2_P_DI_DATA2', 'DLAB_LPR', 'CKPI_P_DATA', 'CFR_P_WORK', 'ACQ_P', 'LRM_P_DATA', 'PBDW_P_FSV_STAGE', 'ECOMM_P', 'EUFIN_P_DATA', 'ACLD_P_DATA', 'PEDW_P_STAR2_JOB', 'SEM_RUCWD', 'AMENA_GTM_P_DATA', 'LMDM_P_CRDM', 'PBDW_P_SFSO_STAGE', 'CNSMR_INSGHT_RSTR_P_DATA', 'FLSDW_P_EMI', 'SYSLIB', 'CKPI_P', 'RUSDA_P_WORK', 'CNSMR_INSGHT_P', 'DLAB_PERF', 'ODW_P', 'SEM_GLBL_FINCL', 'DLAB_CINS', 'VBN_P_CTLSS_DTA', 'PBDW_P_EPAD_JOB', 'tdwm', 'MDW_P_WORK', 'PEDW_P_STAR2_FCST', 'VBN_P', 'SYSUIF', 'SCP_BEV_P', 'PBDW_P_MERCHMBA', 'BPM_P_DATA', 'DMS_P', 'PBDW_P_RME_JOB', 'SEM_PBDW_SCR', 'SLSTALRT_P', 'PEDW_P_STAR2_EXT_VW', 'PBDW_P_PTS_JOB', 'GSFOD_P_FACTS', 'SEM_SUS', 'DLAB_NJTRK', 'PEDW_P_STAR2', 'QTG_SBX_EXTRACT_VW', 'dataworks_dbc_stage', 'PAID_P_UTIL', 'STAR2_P', 'PBF_P', 'DSC_P_STAGE', 'TD_ANALYTICS_DB', 'PDCRADM', 'DLAB_CAPEX', 'AMESA_RM_P_DATA', 'GSFOD_P_STAGE', 'PBDW_P_RPTNG', 'PBDW_P_LGCYVW', 'DWL_BASE', 'IFOD_P_FACTS', 'GDQ_P_SP', 'IIE_P_STAGE', 'DLAB_SCP_PBNA', 'FLSDW_P_APX', 'viewpoint', 'SEM_SLST', 'CAS_TPM_P_MSTR', 'DWL_P_ARCH', 'QTG_P2', '80309254', 'STAR2_P_RBS_WORK', 'PFC_TPM_P', 'ACQ_P_WORK', 'STAR2_P_DI', 'CAS_FM_P', 'baradmin', 'CPPTADM', 'SEM_BEV_OPT', 'ODW_P_UTIL', 'PBDW_P_MAA_WORK', 'Sys_Calendar', 'SUS_P_FACTS', 'ESSA_SCA_BATCH_P', 'GDQ_P_DATA', 'PBDW_P_PMX_STAGE', 'PBC_DL', 'ACQ_P_SEC_UM', 'FL_LGL', 'PBDW_P_WHSS_DATA', 'PBDW_P_INTG_WORK', 'PBDW_P_MAA_DATA', 'SEM_AMESAAPAC', 'SSR_P_STG', 'PBDW_P_RPTNG_JOB', 'QTG_P2_XAPP', 'PQP_P', 'PBDW_P_EPAD_STAGE', 'CNSMR_INSGHT_RSTR_P', 'GSFOD_P_MSTR', 'VBN_P_DFR', 'PEDW_P_STAR2_SCTY', 'SYSUDTLIB', 'PBDW_P_CETS', 'DWL_P_RSTR', 'PBDW_P_KPI_JOB', 'BPL_P_SP', 'PBDW_P_PMX_DATA', 'DLAB_ECOMMERCE', 'MDM_P_UTIL', 'PMM_P_STAGE', 'SEM_AMESA_MVS', 'STAR2_P_DI_DATA1', 'FLSDW_P_UTIL', 'NRM_P_WORK', 'PBDW_P_DSHCCO', 'PBDW_P_CIV', 'PBDW_P_INTG_UTIL', 'ACQ_P_JOB', 'ISCP_P_DATA', 'SEM_ECOMM', 'CNSMR_INSGHT_RSTR_P_STAGE', 'TDaaS_DB', 'SEM_GDQ', 'FPS_P_DATA', 'DLAB_LGHTHSE', 'DLAB_NRM', 'GLBL_COM_P', 'PBF_P_DATA', 'DLAB_EUOMD', 'CPPTINFO', 'PBDW_P_WWPM', 'POR_P', 'EUSCA_P', 'QTG_DLX_VW', 'STAR2_P_FY2012', 'FLSDW_LGL_FACTS', 'PBDW_P_PSC', 'SEM_INSGHT_RSTR', 'DLAB_NAB_DPSTAT', 'ACQ_P_SEC_DIM', 'PEDW_P_STAR2_ASST', 'FLSDW_P', 'ACLD_P_STAGE', 'DLAB_PAID', 'PFC_TPM_P_DATA', 'DMS_P_UTIL', 'DLAB_PBC', 'DLAB_EU_RDA', 'IFOD_P_MSTR', 'PMF_P', 'QTG_SCX_P2_MATV', 'FPS_P_WORK', 'QTG_SBXNABQ_ENDECA', '40019763', 'DMS_P_DATA', 'EXTRCT_P_DATA', 'DBAWORK_FL_P_MSTR_1', 'LATAM_BEV_P', 'PEDW_P_STAR2_PRJCT', 'DBCMANAGER', 'FPS_P_MSTR', 'SEM_HVL', 'FL_P_FACTS', 'CAT_P_WORK', 'NAB_APP_P_DATA', 'ACQ_P_PSTG_UTIL', 'SEM_GLBL_SFOD', 'STAR2_P_FY2013_14_15_DATA', 'STAR2_P_FY2007', 'DATALAB_EUSMD', 'ISCP_P_STAGE', 'SEM_TPO', 'FLNA_APP_P_DATA', 'DSC_P_DATA', 'PBDW_P_CTLFLT_DATA', 'MDM_P', 'PBDW_P_EPAD', 'SEM_PAID', 'APAC_OPEX_P_JOB', 'STAR2_P_CDA_DATA', 'STAR2_P_PNB_WORK', 'PBDW_P_DBA_DATA', 'PBDW_P_ARCV', 'TargetDBName', 'DWL_P_WORK', 'GCA_P_DATA', 'MDM_P_IN', 'GSFOD_P', 'LMDM_P_SRC', 'PBDW_P_PMAX_STAGE', 'VBN_P_MAA_DATA', 'SUS_P', 'POR_P_STAGE', 'SEM_IFOD', 'LMDM_P_UCBKUP', 'PBDW_P_PPM_DATA', 'PEDW_P_STAR2_SYS', 'QTG_SBXNABQ_SUPPLYCHAIN_BASE', 'SEM_PBDW', 'NRM_P_JOB', 'PEDW_P_STAR2_LIST', 'SysAdmin', 'STAR2_P_FY2007_DATA', 'DLAB_DSGN', 'PBDW_P_IPSCR_STAGE', 'SEM_RUSDA', 'DSC_P', 'PMM_P_DATA']

def check_table(obj,layer):
    if len(obj.split(".")) != 2:
        return False
    else:
        if obj.split(".")[0] in database_list or re.search("[$]([A-Z0-9_-{}]+)[.]([A-Z0-9_-{}]+)$",obj.replace(';','')):
            return True
        else:
            return False

def convert_env_variable(table,layer):
    if table.find("$") !=-1 or table.find("{")!=-1:
        x = table.split(".")[0]
        strt_pos = table.find('$')
        end_pos = table.find('}')
        y = table[strt_pos:end_pos+1]
        ENV_VAR = read_env(layer)
        try:
            nw_tb = ENV_VAR[layer.upper()][y] + table[end_pos+1:len(table)+1]
        except:
            return table
        return nw_tb
    else:
        return table

def banalysis(input_list,layer,uploaded_env_fle):
    global uploaded_env_file
    uploaded_env_file = uploaded_env_fle
    lst_of_all_bteqs = []
    j=0
    for i in input_list:
        print(j, end = "    ")
        j+=1
        lst_of_all_bteqs.extend(fun_src_trgt_tbl(i,layer))

    df = pd.DataFrame(lst_of_all_bteqs,columns=['File Name','Source Tables', 'Target Tables','Operation Type'])
    df.drop_duplicates(keep="first", inplace=True)
    # df.replace(df['File Name'],df['File Name'].)
    # df['File Name'].apply(lambda x: x.rsplit('\\'))
    df['File Name'] = df['File Name'].str.split('\\').str[-1]
    return df
    
def fun_src_trgt_tbl(input_file,layer):
    
    # Read the BTEQ fils in read mode
    fw = open(input_file, "r", newline='', encoding="cp437", errors='ignore')
    print(input_file)
    # Read each lines and create a list.Each line of the file is an item of the list
    l_all_lines = fw.readlines()
    l_each_word = []
    l_each_word_remove_space = []
    l_src_tbl = []
    l_trgt_tbl = []

    # Read each line 
    for i in l_all_lines:
        # Remove tab,space,new lines
        l_str = i.strip()
        # Replace , and ( and ) and AS keyword
        l_str = l_str.replace(',',' ')
        l_str = l_str.replace('(',' ')
        l_str = l_str.replace(')',' ')
        l_str = re.sub(r'/bAS/b',' ',l_str)
        # If the line doesn't start with # or -
        if not l_str.startswith(("#", "-")):
            # Break each lines into word and store into a list
            l_each_word.extend(l_str.split(' '))

    for i in l_each_word:
        if i.strip() != '':
            # remove tab,new line,spaces from each word,convert into uppercase and store into another list
            l_each_word_remove_space.append(i.strip().upper())
        
    fw.close()

    k = 0
    cmnt_flg = 'N'
    lst = []
    for i in l_each_word_remove_space:
        # If the word starts with /* code commenting starts.So do not consider any word untill it finds */
        if i.startswith('/*'):
            cmnt_flg = 'Y'
        if i.endswith('*/'):
            cmnt_flg = 'N'
        if i == 'CREATE' and cmnt_flg == 'N':
        
            lv_trgt_tbl =''
            lv_src_tbl = ''
            if l_each_word_remove_space[k+3] == 'TABLE':
            # If the word after insert into follow database.tablename pattern
                lv_trgt_tbl = l_each_word_remove_space[k+4].replace(';','') if check_table(l_each_word_remove_space[k+4].replace(';',''),layer) else ""
            else:
                lv_trgt_tbl = l_each_word_remove_space[k+2].replace(';','') if check_table(l_each_word_remove_space[k+2].replace(';',''),layer) else ""
            
            pos_semi_colon = 0
            pos_from = 0
            
            # Find the first semicolon after insert into
            list_of_semi_colon = [n for n, elem in enumerate(l_each_word_remove_space[k:]) if ';' in elem]
            if len(list_of_semi_colon) > 0:
                pos_semi_colon = min(list_of_semi_colon)
            
            # Find the first from keyword after insert into
            list_of_from = [n for n, elem in enumerate(l_each_word_remove_space[k:]) if 'FROM' in elem]
            if len(list_of_from) > 0:
                pos_from = min(list_of_from)
            
            
            # Find all the tables between from and semicolon which follows database.tablename pattern
            for j in l_each_word_remove_space[k+pos_from : k+pos_semi_colon]:
                if check_table(j.replace(';',''),layer):
                    lv_src_tbl = j.replace(';','')
                    lst.append([input_file.split('/')[-1],convert_env_variable(lv_src_tbl,layer),convert_env_variable(lv_trgt_tbl,layer),'Create'])

            
            #If create statement is not from a table
            if  lv_src_tbl == '':
                lst.append([input_file.split('/')[-1],convert_env_variable(lv_src_tbl,layer),convert_env_variable(lv_trgt_tbl,layer),'Create'])
        
        if i == 'INSERT' and cmnt_flg == 'N':
        
            lv_trgt_tbl =''
            lv_src_tbl = ''
            
            # If the word after insert into follow database.tablename pattern
            lv_trgt_tbl = l_each_word_remove_space[k+2].replace(';','') if check_table(l_each_word_remove_space[k+2].replace(';',''),layer) else ""
            
            pos_semi_colon = 0
            pos_from = 0
            
            # Find the first semicolon after insert into
            list_of_semi_colon = [n for n, elem in enumerate(l_each_word_remove_space[k:]) if ';' in elem]
            if len(list_of_semi_colon) > 0:
                pos_semi_colon = min(list_of_semi_colon)
            
            # Find the first from keyword after insert into
            list_of_from = [n for n, elem in enumerate(l_each_word_remove_space[k:]) if 'FROM' in elem]
            if len(list_of_from) > 0:
                pos_from = min(list_of_from)
            
            # Find all the tables between from and semicolon which follows database.tablename pattern
            for j in l_each_word_remove_space[k+pos_from : k+pos_semi_colon]:
                if check_table(j.replace(';',''),layer):
                    lv_src_tbl = j.replace(';','')
                    
                    lst.append([input_file.split('/')[-1],convert_env_variable(lv_src_tbl,layer),convert_env_variable(lv_trgt_tbl,layer),'Insert'])
                    
            
            #If insert statement is not from a table
            if  lv_src_tbl == '':
                lst.append([input_file.split('/')[-1],convert_env_variable(lv_src_tbl,layer),convert_env_variable(lv_trgt_tbl,layer),'Insert'])
                
        
        if i == 'MERGE' and cmnt_flg == 'N':
        
            lv_trgt_tbl = ''
            lv_src_tbl = ''
            
            # If the word after insert into follow database.tablename pattern
            
            lv_trgt_tbl = l_each_word_remove_space[k+2].replace(';','') if check_table(l_each_word_remove_space[k+2].replace(';',''),layer) else ""
            
            pos_semi_colon = 0
            pos_using = 0
            
            # Find the first semicolon after insert into
            list_of_semi_colon = [n for n, elem in enumerate(l_each_word_remove_space[k:]) if ';' in elem]
            if len(list_of_semi_colon) > 0:
                pos_semi_colon = min(list_of_semi_colon)
            
            # Find the first using key word after insert into
            list_of_using = [n for n, elem in enumerate(l_each_word_remove_space[k:]) if 'USING' in elem]
            if len(list_of_using) > 0:
                pos_using = min(list_of_using)
        

            
            # find all the tables have databasename.tablename between using clause and semicolon
            for j in l_each_word_remove_space[k+pos_using : k+pos_semi_colon]:
                if check_table(j.replace(';',''),layer):
                    lv_src_tbl = j.replace(';','')
                    lst.append([input_file.split('/')[-1],convert_env_variable(lv_src_tbl,layer),convert_env_variable(lv_trgt_tbl,layer),'Merge'])

                
        if i == 'UPDATE' and cmnt_flg == 'N':
            
            lv_trgt_tbl = ''
            lv_src_tbl = ''
            
            # If the word next to update is a table name has database.tablename pattern
            if check_table(l_each_word_remove_space[k+1].replace(';',''),layer):
                lv_trgt_tbl = l_each_word_remove_space[k+1].replace(';','')
            
            # If the update is a corealted subquery
            else:
                try:
                    # Find the alias after update keyword
                    str_alias = l_each_word_remove_space[k+1]
                    # Find the next position of the alias
                    indx = l_each_word_remove_space.index(str_alias,k+2,)
                    # Table name is the word before the alias
                    lv_trgt_tbl = l_each_word_remove_space[indx - 1] if check_table(l_each_word_remove_space[indx - 1].replace(';',''),layer) else ""
                except ValueError:
                    None
            
            # If the target table follow databasename.tablename pattern
            
                
            pos_semi_colon = 0
            pos_from = 0
            
            # Find the postion of 1st semicolon after update keyword
            list_of_semi_colon = [n for n, elem in enumerate(l_each_word_remove_space[k:]) if ';' in elem]
            if len(list_of_semi_colon) > 0:
                pos_semi_colon = min(list_of_semi_colon)
        
            # Find the postion of 1st from keyword after update keyword
            list_of_from = [n for n, elem in enumerate(l_each_word_remove_space[k:]) if 'FROM' in elem]
            if len(list_of_from) > 0:
                pos_from = min(list_of_from)
                

            
            #Find all tables between from and semicolon, follow databasename.tablename pattern
            for j in l_each_word_remove_space[k+pos_from : k+pos_semi_colon]:
                    if check_table(j.replace(';',''),layer):
                        lv_src_tbl = j.replace(';','')
                        lst.append([input_file.split('/')[-1],convert_env_variable(lv_src_tbl,layer),convert_env_variable(lv_trgt_tbl,layer),'Update'])
                        
            
            if  lv_src_tbl == '':
                lst.append([input_file.split('/')[-1],convert_env_variable(lv_src_tbl,layer),convert_env_variable(lv_trgt_tbl,layer),'Update'])

            
        if (i == 'DELETE' or i == 'DEL') and cmnt_flg == 'N':  
        
            lv_trgt_tbl = ''
            lv_src_tbl = ''
            
           
            if check_table(l_each_word_remove_space[k+1].replace(';',''),layer):
                lv_trgt_tbl = l_each_word_remove_space[k+1].replace(';','')
                
            elif check_table(l_each_word_remove_space[k+2].replace(';',''),layer):
                lv_trgt_tbl = l_each_word_remove_space[k+2].replace(';','')
            else:
                try:
                    if l_each_word_remove_space[k+1] == 'FROM':
                        str_alias = l_each_word_remove_space[k+2]
                        indx = l_each_word_remove_space.index(str_alias,k+3,)
                        lv_trgt_tbl = l_each_word_remove_space[indx - 1].replace(';','')
                    else:
                        str_alias = l_each_word_remove_space[k+1]
                        indx = l_each_word_remove_space.index(str_alias,k+2,)
                        lv_trgt_tbl = l_each_word_remove_space[indx - 1].replace(';','')
                except ValueError:
                    None
            if  check_table(lv_trgt_tbl,layer):
                list_of_semi_colon = [n for n, elem in enumerate(l_each_word_remove_space[k:]) if ';' in elem]
                if len(list_of_semi_colon) > 0:
                    pos_semi_colon = min(list_of_semi_colon)
                for j in l_each_word_remove_space[k+3 : k+pos_semi_colon]:
                    if check_table(j.replace(';',''),layer):
                        lv_src_tbl = j.replace(';','')
                        lst.append([input_file.split('/')[-1],convert_env_variable(lv_src_tbl,layer),convert_env_variable(lv_trgt_tbl,layer),'Delete'])    
                if  lv_src_tbl == '':
                    lst.append([input_file.split('/')[-1],convert_env_variable(lv_src_tbl,layer),convert_env_variable(lv_trgt_tbl,layer),'Delete'])
        k = k + 1
    return lst

def bteq_analysis(input_file,layer): 
    try:
        btq_list = exceltolist(input_file)
    except: btq_list = input_file
    banalysis(btq_list,layer)
