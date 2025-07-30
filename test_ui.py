import streamlit as st
import pandas as pd
import os
import SaveAndDelete_uploaded_flie as uf
import search_download as sd
import bteq_analysis as ba
import tbl_info as tb
import Find_Pks as fpk
import glob
from ExcelToList import exceltolist, file_to_list
import tempfile
import RE_BTQ
import viewanalysis as va

# ---- Modular UI Functions ----
def login_ui():
    """Enhanced Login page UI with modern styling."""
    # Custom CSS for styling
    st.markdown("""
        <style>
        /* Background watermark */
        .stApp {
            background-image: 
                radial-gradient(circle at 20% 20%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(118, 75, 162, 0.1) 0%, transparent 50%),
                linear-gradient(45deg, transparent 40%, rgba(102, 126, 234, 0.05) 50%, transparent 60%);
            background-size: 300px 300px, 250px 250px, 100% 100%;
            background-repeat: no-repeat, no-repeat, no-repeat;
            background-position: top left, bottom right, center;
        }
        
        /* Data analytics watermark pattern */
        .stApp::before {
            content: "📊 📈 📉 💹 📋 🔍 ⚙️ 🖥️ 📊 📈 📉 💹 📋 🔍 ⚙️ 🖥️";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            font-size: 24px;
            opacity: 0.03;
            pointer-events: none;
            z-index: -1;
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-around;
            line-height: 3;
        }
        
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            text-align: center;
            margin-top: 2rem;
            position: relative;
            z-index: 1;
        }
        .login-title {
            color: white;
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            white-space: nowrap;
            line-height: 1.2;
        }
        .login-subtitle {
            color: rgba(255,255,255,0.9);
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
            text-align: center;
            margin-left: auto;
            margin-right: auto;
        }
        .welcome-text {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            color: white;
            font-size: 0.95rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Create centered login container
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Company logo in gradient container
        st.markdown("""
        <div class="login-container">
            <!-- Company logo inside the gradient container -->
            <img src="https://latestlogo.com/wp-content/uploads/2024/02/cognizant.png" width="180" style="margin-bottom: 0;">
        </div>
        """, unsafe_allow_html=True)
        
        # Title and subtitle outside gradient
        st.markdown('<h1 class="login-title">Data Analytics Hub</h1>', unsafe_allow_html=True)
        st.markdown('<p class="login-subtitle">Secure Access Portal</p>', unsafe_allow_html=True)
        
        # Welcome message outside gradient
        st.markdown("""
            <div class="welcome-text">
                🔐 Welcome to the Data Analytics Platform<br>
                Please enter your credentials to continue
            </div>
        """, unsafe_allow_html=True)
        
        # Login form with enhanced styling
        st.markdown("### 🚀 Login to Continue")
        
        # Input fields with icons
        username = st.text_input(
            "👤 Username",
            placeholder="Enter your username",
            help="Use 'admin' for demo access"
        )
        
        password = st.text_input(
            "🔑 Password",
            type="password",
            placeholder="Enter your password",
            help="Use 'password' for demo access"
        )
        
        # Login button with enhanced styling
        if st.button("🔓 Login", type="primary", use_container_width=True):
            if not username:
                st.warning("⚠️ Please enter your username")
            elif not password:
                st.warning("⚠️ Please enter your password")
            elif check_login(username, password):
                st.success("✅ Login successful! Redirecting...")
                st.balloons()
                st.session_state["logged_in"] = True
                st.session_state.page = "main"
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
        
        # Additional info section
        with st.expander("ℹ️ Demo Credentials"):
            st.info("""
                **For demonstration purposes:**
                - **Username:** admin
                - **Password:** password
                
                🛡️ This is a secure data analytics platform for data engineering and analysis tasks.
            """)
        
        # Footer
        st.markdown("---")
        st.markdown(
            "<div style='text-align: center; color: #666; font-size: 0.8rem;'>"
            "🏢 Cognizant Data Analytics Platform | Secure & Reliable"
            "</div>", 
            unsafe_allow_html=True
        )

def main_ui():
    """Main tool selection UI."""

    # Add a logo/image
    logo_url = "https://latestlogo.com/wp-content/uploads/2024/02/cognizant.png" 
    st.image(logo_url, width=200)

    # Use colorful containers
    with st.container():
        st.title("About this App")
        st.markdown("""
        This web application provides a suite of data analysis tools to streamline your workflow. Easily search, analyze, and retrieve data using a user-friendly interface. Select a tool from the sidebar to begin.
        """)
        st.markdown("""
        ### Tool Descriptions
        - **Search & Download Files**: 
            - Search for files on a remote server using flexible patterns and download selected files directly to your local system. Supports bulk selection and progress feedback.
        - **BTEQ Analysis**: 
            - Upload BTEQ scripts and (optionally) environment files for automated analysis. Get structured output and insights from your batch scripts. Designed for Teradata BTEQ workloads.
        - **Table Schema Info**: 
            - Retrieve schema and DDL information for one or more database tables. Enter table names (with schema) to get detailed metadata and structure information.
        """)
        st.info("Use the sidebar to navigate between tools.")

def tbl_info_ui():
    """Enhanced Table Schema Info UI with modern styling."""
    # Add custom CSS for this page
    st.markdown("""
        <style>
        /* Remove default spacing at top of page */
        .main .block-container {
            padding-top: 1rem !important;
        }
        .env-header {
            background: rgba(40, 167, 69, 0.05);
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            border: 1px solid rgba(40, 167, 69, 0.2);
            margin-bottom: 1rem;
        }
        .credentials-section {
            background: rgba(102, 126, 234, 0.05);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid rgba(102, 126, 234, 0.2);
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("📋 Table Schema Information Center")
    st.markdown("*Explore database schemas and table structures across environments*")
    
    # Environment selection with enhanced styling
    st.markdown("""
        <div class="env-header" style="text-align: center; padding: 0rem;">
            <h3 style="margin: 0; color: #28a745;">🌍 Environment Selection</h3>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("Choose your target Teradata environment for schema analysis")
    st.markdown('</div>', unsafe_allow_html=True)
    
    environment = st.segmented_control(
        label="🔍 Select Teradata Environment:",
        options=["qa", "prod", "dev"],
        format_func=lambda x: f"🟡 {x.upper()}" if x == "qa" else f"🔴 {x.upper()}" if x == "prod" else f"🟢 {x.upper()}",
        default="qa",
        selection_mode="single",
        help="ℹ️ **QA**: Testing environment | **PROD**: Production environment | **DEV**: Development environment"
    )
    
    # Enhanced environment info
    env_info = {
        "qa": {"color": "🟡", "desc": "Quality Assurance - Safe for testing", "host": "tdplqa.corp.pep.pvt"},
        "prod": {"color": "🔴", "desc": "Production - Live data environment", "host": "tdplprod.corp.pep.pvt"},
        "dev": {"color": "🟢", "desc": "Development - Experimental environment", "host": "tdpldev.corp.pep.pvt"}
    }
    
    st.success(f"{env_info[environment]['color']} **{environment.upper()} Environment Selected**\n\n📍 {env_info[environment]['desc']}\n🔗 Host: `{env_info[environment]['host']}`")
    
    # Enhanced Teradata Credentials section
    st.markdown("""
        <div class="credentials-section" style="text-align: center; padding: 0rem;">
            <h3 style="margin: 0;color: #17a2b8; ">🔐 Authentication Credentials</h3>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("🔒 *Secure login to access Teradata schema information*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        td_username = st.text_input(
            "👤 Teradata User ID",
            placeholder="e.g., 12345678 or username",
            help="📝 **Employee ID Format**: 8-digit number (uses LDAP)\n📝 **Username Format**: Standard username (uses basic auth)",
            label_visibility="visible"
        )
    
    with col2:
        td_password = st.text_input(
            "🔑 Password",
            type="password",
            placeholder="Enter your secure password",
            help="🔒 Your Teradata account password - kept secure and encrypted",
            label_visibility="visible"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Enhanced Table Input Section with segmented control
    st.markdown("### 📋 Database Object Configuration")
    
    # Input method selection with segmented control
    table_input_method = st.segmented_control(
        "🔄 Select Input Method:",
        options=["Manual Input", "File Input"],
        default="Manual Input",
        help="📝 **Manual Input**: Type table names directly\n📁 **File Input**: Upload Excel/CSV/TXT file"
    )
    
    tbl_nm_lst = []
    if table_input_method == "File Input":
        # File upload option
        st.markdown("📁 **Upload file containing database object names**")
        uploaded_table_file = st.file_uploader(
            "📁 Choose File (Excel/CSV/TXT)",
            type=['xlsx', 'xls', 'csv', 'txt'],
            accept_multiple_files=False,
            help="📄 **Supported**: .xlsx, .xls, .csv, .txt\n📝 **Format**: One table name per row or comma-separated\n📈 **Excel**: First column will be used"
        )
        
        if uploaded_table_file is not None:
            try:
                # Use the unified file_to_list function
                tbl_nm_lst = file_to_list(uploaded_table_file, uploaded_table_file.name)
                
                if tbl_nm_lst:
                    st.success(f"✅ **File processed!** Found {len(tbl_nm_lst)} table names")
                    with st.expander(f"🔍 Preview ({len(tbl_nm_lst)} items)"):
                        for i, name in enumerate(tbl_nm_lst[:10]):
                            st.markdown(f"• `{name}`")
                        if len(tbl_nm_lst) > 10:
                            st.markdown(f"... and {len(tbl_nm_lst) - 10} more")
                else:
                    st.warning("⚠️ No valid table names found in file")
                    
            except Exception as e:
                st.error(f"❌ **Error processing file**: {str(e)}")
                tbl_nm_lst = []
    else:
        # Manual input option (original)
        tbl_nm_str = st.text_area(
            "📦 Database Objects (Tables/Views)",
            placeholder="Enter one or more database objects separated by commas:\n\nExamples:\n• ACQ_P_DIM.PGT_ORDR_MSTR_DAT\n• DWL_P_BASE.PGT_OPS_PROD_ORDER\n• SCHEMA_NAME.TABLE_NAME",
            value="ACQ_P_DIM.PGT_ORDR_MSTR_DAT, DWL_P_BASE.PGT_OPS_PROD_ORDER",
            height=100,
            help="📝 **Format**: `SCHEMA.TABLE_NAME`\n📝 **Multiple Objects**: Separate with commas\n📝 **Auto-conversion**: Production names automatically converted for QA",
            label_visibility="visible"
        )
        tbl_nm_lst = [x.strip() for x in tbl_nm_str.split(",") if x.strip()]
    
    # Auto-convert database names for QA environment with enhanced display
    if environment == 'qa' and tbl_nm_lst:
        st.markdown("#### 🔄 QA Environment Auto-Conversion")
        converted_tbl_lst = []
        conversions_made = []
        
        for table_name in tbl_nm_lst:
            # Case-insensitive replacement of '_P_' with '_S1_'
            if '_p_' in table_name.lower():
                original_name = table_name
                import re
                converted_name = re.sub(r'_[pP]_', '_S1_', table_name)
                converted_tbl_lst.append(converted_name)
                if converted_name != original_name:
                    conversions_made.append((original_name, converted_name))
            else:
                converted_tbl_lst.append(table_name)
        
        if conversions_made:
            st.info("🔄 **Automatic Production → QA Conversion Applied**")
            # for orig, conv in conversions_made:
            #     st.markdown(f"• `{orig}` → `{conv}`")
        else:
            st.success("✅ No conversion needed - objects already in QA format")
            
        tbl_nm_lst = converted_tbl_lst
    
    # Enhanced action button with validation
    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    
    with col_btn2:
        if st.button(
            "🚀 Analyze Table Schemas", 
            type="primary", 
            use_container_width=True,
            help="Connect to Teradata and retrieve detailed schema information"
        ):
            if not tbl_nm_lst:
                st.error("⚠️ **Missing Objects**: Please enter at least one database object name")
            elif not td_username:
                st.error("⚠️ **Missing User ID**: Please enter your Teradata User ID")
            elif not td_password:
                st.error("⚠️ **Missing Password**: Please enter your Teradata password")
            else:
                with st.spinner(f"🔍 Analyzing schemas in {environment.upper()} environment..."):
                    tbl_info_df = tb.table_size_ddl(
                        tbl_nm_lst, 
                        environment=environment, 
                        username=td_username, 
                        password=td_password
                    )
                st.success(f"✅ **Analysis Complete!** Retrieved schema information from {environment.upper()} environment")
                st.markdown("### 📊 Schema Analysis Results")
                st.dataframe(
                    tbl_info_df, 
                    hide_index=True,
                    use_container_width=True
                )

def bteq_analysis_ui():
    """Enhanced BTEQ Analysis UI with modern styling."""
    # Custom CSS for BTEQ Analysis page
    st.markdown("""
        <style>
        /* Remove default spacing at top of page */
        .main .block-container {
            padding-top: 1rem !important;
        }
        .bteq-header {
            background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 0.1rem;
            border-radius: 12px;
            border-left: 4px solid #28a745;
            margin-bottom: 1.5rem;
        }
        .layer-section {
            background: rgba(40, 167, 69, 0.05);
            padding: 1.5rem;
            border-radius: 10px;
            border: 1px solid rgba(40, 167, 69, 0.2);
            margin: 1rem 0;
        }
        .upload-section {
            background: rgba(102, 126, 234, 0.05);
            padding: 1.5rem;
            border-radius: 10px;
            border: 1px solid rgba(102, 126, 234, 0.2);
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("⚙️ BTEQ Analysis Center")
    st.markdown("*Analyze BTEQ scripts, dependencies, and data flow patterns*")
    
    # Layer selection with enhanced styling
    st.markdown("""
        <div class="layer-section" style="text-align: center; padding: 0rem;">
            <h3 style="margin: 0; color: #28a745;">🏷️ Data Layer Selection</h3>
        </div>
    """, unsafe_allow_html=True)
    
    layer_descriptions = {
        "APP": "📱 Application Layer - Business logic and presentation layer",
        "DWL": "🏢 Data Warehouse Layer - Data transformation and aggregation", 
        "ACQ": "📊 Acquisition Layer - Raw data ingestion and initial processing"
    }
    
    layer = st.selectbox(
        "🎯 Select Data Architecture Layer:",
        ["APP", "DWL", "ACQ"],
        help="📝 **APP**: Application/Business layer with complex logic\n📝 **DWL**: Data Warehouse layer for analytics\n📝 **ACQ**: Data Acquisition layer for ingestion",
        format_func=lambda x: f"{x} - {layer_descriptions[x].split(' - ')[1]}"
    )
    
    st.info(layer_descriptions[layer])
    # st.markdown('</div>', unsafe_allow_html=True)
    
    uploaded_env_file_path = ''
    
    # Environment file upload for APP layer
    if layer == 'APP':
        st.markdown("""
        <div class="upload-section" style="text-align: center; padding: 0rem;">
            <h3 style="margin: 0;color: #17a2b8;">📜 Environment Configuration</h3>
        </div>
    """, unsafe_allow_html=True)
        st.markdown("⚠️ *Required for APP layer analysis*")
        
        uploaded_env_file = st.file_uploader(
            label="📁 Upload Environment Configuration File",
            type=['ksh', 'txt', 'sh', 'env'],
            accept_multiple_files=False,
            help="📄 **Required for APP layer**: Upload your environment file (.ksh, .sh, .txt, .env)\n🔍 **Contains**: Database names, connection strings, environment variables"
        )
        
        if uploaded_env_file:
            st.success(f"✅ Environment file uploaded: `{uploaded_env_file.name}`")
            uploaded_env_file = [uploaded_env_file]
            uploaded_env_file_path_list = uf.save_uploaded_files(uploaded_env_file)
            uploaded_env_file_path = uploaded_env_file_path_list[0]
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # BTEQ files upload section
    st.markdown("""
        <div class="upload-section" style="text-align: center; padding: 0rem;">
            <h3 style="margin: 0;color: #17a2b8;">📊 BTEQ Script Files</h3>
        </div>
    """, unsafe_allow_html=True)
    # st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    # st.markdown("### 📊 BTEQ Script Files")
    st.markdown("📦 *Upload your BTEQ scripts for comprehensive analysis*")
    
    input_list = st.file_uploader(
        "📁 Select BTEQ Script Files",
        type=['btq', 'bteq', 'sh', 'ksh', 'sql'],
        accept_multiple_files=True,
        help="📄 **Supported formats**: .btq, .bteq, .sh, .ksh, .sql\n📊 **Multiple files**: Upload all related scripts for complete analysis\n🔍 **Analysis**: Extracts tables, dependencies, and data flow"
    )
    
    if input_list:
        st.success(f"✅ {len(input_list)} file(s) uploaded successfully")
        # for file in input_list:
        #     st.markdown(f"• `{file.name}` ({file.size:,} bytes)")
        input_list = uf.save_uploaded_files(input_list)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced analysis button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        analysis_clicked = st.button(
            "🚀 Start Comprehensive Analysis", 
            type="primary", 
            use_container_width=True,
            help="Begin detailed analysis of uploaded BTEQ scripts"
        )
    
    # Results display outside column structure for full width
    if analysis_clicked:
        if not input_list:
            st.error("⚠️ **No Files Uploaded**: Please upload at least one BTEQ file")
        else:
            with st.spinner("🔍 Running comprehensive analysis..."):
                bteq_analysis_df = ba.banalysis(input_list, layer, uploaded_env_file_path)
            st.session_state.bteq_analysis_df = bteq_analysis_df
            # st.success("✅ **Analysis Complete!** BTEQ scripts analyzed successfully")
            st.markdown("### 📉 Analysis Results")
            st.dataframe(
                st.session_state.bteq_analysis_df,
                hide_index=True,
                use_container_width=True
            )
        # Clean up
        for path in input_list:
            uf.delete_uploaded_files(path)
        if uploaded_env_file_path:
            uf.delete_uploaded_files(uploaded_env_file_path)
        # st.success(f"All files deleted successfully.")

def search_ui():
    """Enhanced File Search UI with modern styling."""
    # Custom CSS for Search page
    st.markdown("""
        <style>
        /* Remove default spacing at top of page */
        .main .block-container {
            padding-top: 1rem !important;
        }
        .ssh-section {
            background: rgba(220, 53, 69, 0.05);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid rgba(220, 53, 69, 0.2);
            margin: 1rem 0;
        }
        .search-section {
            background: rgba(23, 162, 184, 0.05);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid rgba(23, 162, 184, 0.2);
            margin: 1rem 0;
        }
        .server-info {
            background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #dc3545;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🔍 File Search & Download Center")
    st.markdown("*Search and download files from remote servers via secure SSH connection*")
    
    # SSH Connection Details with enhanced styling
    st.markdown("""
        <div class="ssh-section" style="text-align: center; padding: 0.1rem;">
            <h3 style="margin: 0; color: white;">🔐 SSH Server Connection</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("🔒 *Secure connection to remote file servers*")
    
    # Server connection info in white/gray box
    st.markdown("""
        <div class="server-info">
            <p style="margin: 0; font-weight: 500; color: #2c3e50;">🌐 <strong>Connection Details</strong>: Configure your SSH server access credentials</p>
        </div>
    """, unsafe_allow_html=True)
    
    # First row: Hostname and Port
    col1, col2 = st.columns([3, 1])
    with col1:
        hostname = st.text_input(
            "🌍 Server Hostname/IP",
            placeholder="e.g., server.company.com or 192.168.1.100",
            value="peplap00726.corp.pep.pvt",
            help="🔗 **Server Address**: Enter the hostname or IP address of your SSH server\n🔍 **Format**: Can be FQDN or IP address",
            label_visibility="visible"
        )
    with col2:
        port = st.number_input(
            "🔌 SSH Port",
            min_value=1,
            max_value=65535,
            value=22,
            help="🔌 **Default**: Port 22 (standard SSH)\n🔗 **Custom**: Use custom port if configured",
            label_visibility="visible"
        )
    
    # Second row: Username and Password
    col3, col4 = st.columns(2)
    with col3:
        username = st.text_input(
            "👤 SSH Username",
            placeholder="Enter your SSH username",
            help="👤 **Account**: Your SSH login username\n🔐 **Access**: Must have file system permissions",
            label_visibility="visible"
        )
    with col4:
        password = st.text_input(
            "🔑 SSH Password",
            type="password",
            placeholder="Enter your secure password",
            help="🔒 **Security**: Password is encrypted during transmission\n🔐 **Access**: Must match SSH account password",
            label_visibility="visible"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Enhanced File Search Configuration
    st.markdown("""
        <div class="search-section" style="text-align: center; padding: 0.1rem;">
            <h3 style="margin: 0; color: #17a2b8;">📁 File Search Configuration</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("🔍 *Configure your file search parameters and patterns*")
    path = st.text_input(
        "📂 Server Directory Path",
        placeholder="e.g., /etlapps/prds2/acq/stg/TgtFiles/ or /home/user/data/",
        value="/etlapps/prds2/acq/stg/TgtFiles/",
        help="🗺️ **Full Path**: Enter the complete directory path on the server\n📁 **Format**: Unix-style path with forward slashes\n🔍 **Example**: `/data/files/` or `/home/user/documents/`",
        label_visibility="visible"
    )
    
    # Input method selection for filename patterns
    pattern_input_method = st.segmented_control(
        "🔄 Select Pattern Input Method:",
        options=["Manual Input", "File Input"],
        default="Manual Input",
        key="pattern_method",
        help="📝 **Manual Input**: Type patterns directly\n📁 **File Input**: Upload Excel/CSV/TXT file"
    )
    
    pattern_list = []
    if pattern_input_method == "File Input":
        # File upload option
        st.markdown("📁 **Upload file containing filename patterns**")
        uploaded_pattern_file = st.file_uploader(
            "📁 Choose Pattern File (Excel/CSV/TXT)",
            type=['xlsx', 'xls', 'csv', 'txt'],
            accept_multiple_files=False,
            key="pattern_uploader",
            help="📄 **Supported**: .xlsx, .xls, .csv, .txt\n📝 **Format**: One filename pattern per row or comma-separated\n📈 **Excel**: First column will be used"
        )
        
        if uploaded_pattern_file is not None:
            try:
                # Use the unified file_to_list function
                pattern_list = file_to_list(uploaded_pattern_file, uploaded_pattern_file.name)
                
                if pattern_list:
                    st.success(f"✅ **File processed!** Found {len(pattern_list)} filename patterns")
                    with st.expander(f"🔍 Preview ({len(pattern_list)} items)"):
                        for i, pattern in enumerate(pattern_list[:10]):
                            st.markdown(f"• `{pattern}`")
                        if len(pattern_list) > 10:
                            st.markdown(f"... and {len(pattern_list) - 10} more")
                else:
                    st.warning("⚠️ No valid filename patterns found in file")
                    
            except Exception as e:
                st.error(f"❌ **Error processing file**: {str(e)}")
                pattern_list = []
    else:
        # Manual input option (original)
        tptfile = st.text_area(
            "🔍 Filename Search Patterns",
            placeholder="Enter filename patterns (one per line or comma-separated):\n\nExamples:\n• pgt_zggl_otc_cvi_billing_hdr\n• data_export_*.csv\n• report_2024*.xlsx",
            value="pgt_zggl_otc_cvi_billing_hdr",
            height=100,
            help="🔍 **Patterns**: Use wildcards (*) for flexible matching\n📁 **Multiple**: Enter multiple patterns separated by commas\n📄 **Examples**: `file*.txt`, `report_*.csv`, `data_2024*`",
            label_visibility="visible"
        )
        pattern_list = [x.strip() for x in tptfile.split(',') if x.strip()]
    
    # Enhanced search mode toggle
    st.markdown("#### 🔄 Search Mode Configuration")
    
    col_toggle1, col_toggle2 = st.columns([2.9, 8])
    
    with col_toggle1:
        flag = st.toggle(
            "🔍 Smart Search",
            value=True,
            help="✅ **Enabled**: Search for files matching patterns\n❌ **Disabled**: Use exact filenames (skip search)"
        )
    
    with col_toggle2:
        if flag:
            st.success("✅ **Smart Search Enabled** - Will search for files matching your patterns")
        else:
            st.info("📝 **Direct Mode** - Will use exact filenames (faster if you know exact names)")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Use pattern_list from segmented control
    file_list = pattern_list
    out_df = pd.DataFrame(columns=['TimeStamp','Size','Filename'])
    
    # Enhanced search button with validation
    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    
    with col_btn2:
        if st.button(
            "🚀 Start File Search", 
            type="primary", 
            use_container_width=True,
            help="Connect to SSH server and search for files matching your patterns"
        ):
            # Enhanced validation with better error messages
            if not hostname:
                st.error("⚠️ **Missing Hostname**: Please enter the SSH server hostname or IP address")
            elif not username:
                st.error("⚠️ **Missing Username**: Please enter your SSH username")
            elif not password:
                st.error("⚠️ **Missing Password**: Please enter your SSH password")
            elif not path:
                st.error("⚠️ **Missing Path**: Please enter the server directory path")
            elif not file_list:
                st.error("⚠️ **Missing Patterns**: Please enter at least one filename pattern")
            else:
                # All validation passed, perform the search
                if flag:
                    with st.spinner("🔍 Searching files on server..."):
                        try:
                            for file in file_list:
                                # Pass SSH credentials to search function
                                out_file_df = sd.search_files(path, username, file, hostname, port, password)
                                out_df = pd.concat([out_df, out_file_df], ignore_index=True)
                            st.success(f"✅ **Search Complete!** Found {len(out_df)} files matching your patterns")
                        except Exception as e:
                            st.error(f"❌ **Search Failed**: {str(e)}")
                            return
                else:
                    out_df = pd.DataFrame(file_list, columns=['Filename'])
                    st.info("📄 **Simple Search Mode**: Displaying filename patterns (Smart Search disabled)")
            
            if not out_df.empty:
                # Store all data in session state for download page
                st.session_state.out_df = out_df
                st.session_state.path = path
                st.session_state.tptfile = tptfile
                st.session_state.username = username
                st.session_state.hostname = hostname
                st.session_state.port = port
                st.session_state.password = password
                st.session_state.flag = flag
                st.success("Files found and saved in session.")
                st.session_state.page = "download"
                st.rerun()
            else:
                st.info("No matching files found.")

def download_ui():
    """Enhanced File Download UI with modern styling."""
    # Custom CSS for Download page
    st.markdown("""
        <style>
        /* Remove default spacing at top of page */
        .main .block-container {
            padding-top: 1rem !important;
        }
        .download-header {
            background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #28a745;
            margin-bottom: 1.5rem;
        }
        .files-section {
            background: rgba(40, 167, 69, 0.05);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid rgba(40, 167, 69, 0.2);
            margin: 1rem 0;
        }
        .download-config {
            background: rgba(102, 126, 234, 0.05);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid rgba(102, 126, 234, 0.2);
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title row with back button
    col_title1, col_title2 = st.columns([6.5, 2])
    
    with col_title1:
        st.title("📥 File Download Center")
        st.markdown("*Download selected files from the remote server to your local machine*")
    
    with col_title2:
        st.markdown("<br>", unsafe_allow_html=True)  # Add some vertical spacing
        if st.button("⬅️ Back to Search", type="secondary", help="Return to file search page", use_container_width=True):
            st.session_state.page = "search"
            st.rerun()
    
    # Get session data
    out_df = st.session_state.out_df
    path = st.session_state.path
    username = st.session_state.username
    hostname = st.session_state.hostname
    port = st.session_state.port
    password = st.session_state.password
    
    # Search results display
    st.markdown('<div class="download-header">', unsafe_allow_html=True)
    st.markdown(f"### 📁 Search Results from `{hostname}`")
    st.markdown(f"🗺️ **Server Path**: `{path}` | 📄 **Files Found**: {len(out_df)} files")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Files display section
    st.markdown('<div class="files-section">', unsafe_allow_html=True)
    st.markdown("### 📊 Available Files")
    
    if not out_df.empty:
        st.dataframe(
            out_df, 
            hide_index=True,
            use_container_width=True,
            column_config={
                "Filename": st.column_config.TextColumn("📄 Filename", width="large"),
                "Size": st.column_config.TextColumn("📏 Size", width="small"),
                "TimeStamp": st.column_config.TextColumn("🕰️ Modified", width="medium")
            }
        )
    else:
        st.warning("⚠️ No files found in the search results.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # File selection section
    st.markdown('<div class="download-config">', unsafe_allow_html=True)
    st.markdown("### 🎤 File Selection")
    
    file_list = out_df["Filename"].tolist()
    if 'selected_files' not in st.session_state:
        st.session_state.selected_files = []
    
    # Enhanced select all option
    col_select1, col_select2 = st.columns([1, 3])
    
    with col_select1:
        select_all = st.checkbox(
            "✅ Select All Files",
            help="📊 Select or deselect all available files at once"
        )
    
    with col_select2:
        if select_all:
            st.session_state.selected_files = file_list
            st.success(f"✅ All {len(file_list)} files selected for download")
        else:
            if len(st.session_state.selected_files) == len(file_list):
                st.session_state.selected_files = []
    
    # Multi-select with enhanced styling
    selected = st.multiselect(
        "📦 Choose files to download:",
        file_list,
        default=st.session_state.selected_files,
        help="📝 Select individual files you want to download to your local machine",
        label_visibility="visible"
    )
    st.session_state.selected_files = selected
    
    # Download path configuration
    st.markdown("#### 🗺️ Download Destination")
    localpath = st.text_input(
        "📁 Local Download Directory",
        placeholder="e.g., C:/Downloads/ or /home/user/downloads/",
        value="C:/Users/2122693/OneDrive - Cognizant/NewApps2025/test_ui/",
        help="📂 **Local Path**: Enter the full path where files will be saved\n🗺️ **Format**: Use forward slashes or backslashes\n📁 **Auto-create**: Directory will be created if it doesn't exist",
        label_visibility="visible"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    # Enhanced download button
    st.markdown("---")
    col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
    
    with col_dl2:
        if st.button(
            f"📥 Download {len(selected)} Selected Files" if selected else "📥 Download Files",
            type="primary",
            use_container_width=True,
            disabled=not selected,
            help="Download selected files to your local directory with progress tracking"
        ):
            if not selected:
                st.error("⚠️ **No Files Selected**: Please select at least one file to download")
            elif not localpath:
                st.error("⚠️ **Missing Path**: Please specify a local download directory")
            else:
                # All validation passed, start download
                progress_bar = st.progress(0)
                status_text = st.empty()
                status_placeholder = st.empty()
                
                def progress_callback(transferred, total):
                    percent = int((transferred / total if total else 0) * 100)
                    progress_bar.progress(percent)
                    status_text.write(
                        f"{transferred/1024:.2f} / {total/1024:.2f} KB "
                        f"({percent:.2f}%)"
                    )
                
                def status_callback(msg):
                    status_placeholder.write(msg)
                
                with st.spinner("📥 Downloading files..."):
                    try:
                        faulty = sd.download_files(
                            path, username, localpath, selected,
                            hostname, port, password,
                            progress_callback=progress_callback,
                            status_callback=status_callback
                        )
                        
                        if faulty:
                            st.warning(f"⚠️ **Partial Success**: Some files failed to download: {faulty}")
                            st.success(f"✅ **Downloaded**: {len(selected) - len(faulty)} out of {len(selected)} files")
                        else:
                            st.success(f"✅ **Download Complete!** All {len(selected)} files downloaded successfully to `{localpath}`")
                            
                    except Exception as e:
                        st.error(f"❌ **Download Failed**: {str(e)}")
                        progress_bar.empty()
                        status_text.empty()
                        status_placeholder.empty()


def bteq_search_ui():
    """Enhanced BTEQ Search UI for searching BTEQ files from SSH server."""
    import pandas as pd
    
    # Custom CSS for BTEQ Search page
    st.markdown("""
        <style>
        /* Remove default spacing at top of page */
        .main .block-container {
            padding-top: 1rem !important;
        }
        .bteq-search-section {
            background: rgba(255, 152, 0, 0.05);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #ff9800;
            margin-bottom: 1.5rem;
        }
        .search-header {
            background: linear-gradient(90deg, #ff9800 0%, #ffb74d 100%);
            color: white;
            padding: 0rem;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .input-section {
            background: rgba(255, 255, 255, 0.8);
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            margin-bottom: 1rem;
        }.ssh-section {
            background: rgba(220, 53, 69, 0.05);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid rgba(220, 53, 69, 0.2);
            margin: 1rem 0;
        }
        .server-info {
            background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #dc3545;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Page header
    # st.markdown('<div class="search-header">', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: left;">
            <h1 style="color: white; margin: 0; font-size: 2.5rem;">🔍 BTEQ File Search</h1>
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.markdown('Search BTEQ files from SSH server for given database objects')
    
    # SSH Connection Section
    # st.markdown('<div class="bteq-search-section">', unsafe_allow_html=True)
    # SSH Connection Details with enhanced styling
    st.markdown("""
        <div class="ssh-section" style="text-align: center; padding: 0.1rem;">
            <h3 style="margin: 0; color: white;">🔐 SSH Server Connection</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("🔒 *Secure connection to remote file servers*")
    
    # Server connection info in white/gray box
    st.markdown("""
        <div class="server-info">
            <p style="margin: 0; font-weight: 500; color: #2c3e50;">🌐 <strong>Connection Details</strong>: Configure your SSH server access credentials</p>
        </div>
    """, unsafe_allow_html=True)
    
    # First row: Hostname and Port
    col1, col2 = st.columns([3, 1])
    with col1:
        hostname = st.text_input(
            "🌍 Server Hostname/IP",
            placeholder="e.g., server.company.com or 192.168.1.100",
            value="peplap00726.corp.pep.pvt",
            help="🔗 **Server Address**: Enter the hostname or IP address of your SSH server\n🔍 **Format**: Can be FQDN or IP address",
            label_visibility="visible"
        )
    with col2:
        port = st.number_input(
            "🔌 SSH Port",
            min_value=1,
            max_value=65535,
            value=22,
            help="🔌 **Default**: Port 22 (standard SSH)\n🔗 **Custom**: Use custom port if configured",
            label_visibility="visible"
        )
    
    # Second row: Username and Password
    col3, col4 = st.columns(2)
    with col3:
        username = st.text_input(
            "👤 SSH Username",
            placeholder="Enter your SSH username",
            help="👤 **Account**: Your SSH login username\n🔐 **Access**: Must have file system permissions",
            label_visibility="visible"
        )
    with col4:
        password = st.text_input(
            "🔑 SSH Password",
            type="password",
            placeholder="Enter your secure password",
            help="🔒 **Security**: Password is encrypted during transmission\n🔐 **Access**: Must match SSH account password",
            label_visibility="visible"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # BTEQ Search Configuration Section
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown("### 📁 BTEQ Search Configuration")
    st.markdown("🔍 *Configure your BTEQ search parameters*")
    
    # Server Path Input
    path = st.text_input(
        "📂 Server Directory Path",
        placeholder="e.g., /root/dir1/acq/ or /home/user/bteq/",
        value="/root/dir1/acq/",
        help="🗺️ **BTEQ Path**: Directory path where BTEQ files are located\n📁 **Format**: Unix-style path with forward slashes\n🔍 **Examples**: `/root/dir1/acq/`, `/home/dwl/scripts/`",
        label_visibility="visible"
    )
    
    # Layer Selection
    layer = st.selectbox(
        "🏧 Data Layer",
        options=["ACQ", "DWL", "APP"],
        index=0,
        help="📋 **Layer Type**: Select the data layer you're working with\n🔄 **ACQ**: Acquisition layer\n📊 **DWL**: Data Warehouse layer\n📦 **APP**: Application layer",
        label_visibility="visible"
    )
    
    # Environment file upload for APP layer
    uploaded_env_file = None
    if layer == "APP":
        st.markdown("#### 📄 Environment File Upload")
        st.markdown("🔧 *Upload environment file for APP layer configuration*")
        
        uploaded_env_file = st.file_uploader(
            "📁 Environment File (.txt)",
            type=['txt'],
            accept_multiple_files=False,
            help="📄 **Required for APP layer**: Upload environment configuration file\n📝 **Format**: Text file with environment variables\n🔧 **Example**: TD_ENV_PGT.txt",
            key="env_file_uploader"
        )
        
        if uploaded_env_file is not None:
            st.success(f"✅ **Environment file uploaded**: {uploaded_env_file.name}")
            # Save the uploaded file temporarily
            import tempfile
            import os
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
                tmp_file.write(uploaded_env_file.getvalue())
                uploaded_env_file = tmp_file.name
        elif layer == "APP":
            st.warning("⚠️ **Environment file required**: Please upload an environment file for APP layer")
    
    # Note: Process username will be the same as SSH username
    
    # Database Objects Input with segmented control
    st.markdown("#### 📋 Database Objects to Search")
    
    # Input method selection for database objects
    objects_input_method = st.segmented_control(
        "🔄 Select Input Method:",
        options=["Manual Input", "File Input"],
        default="Manual Input",
        help="📝 **Manual Input**: Type object names directly\n📁 **File Input**: Upload Excel/CSV/TXT file"
    )
    
    input_file_list = []
    if objects_input_method == "File Input":
        # File upload option
        st.markdown("📁 **Upload file containing database object names**")
        uploaded_objects_file = st.file_uploader(
            "📁 Choose File (Excel/CSV/TXT)",
            type=['xlsx', 'xls', 'csv', 'txt'],
            accept_multiple_files=False,
            help="📄 **Supported**: .xlsx, .xls, .csv, .txt\n📝 **Format**: One object name per row or comma-separated\n📈 **Example**: ACQ_P_CORE.TABLE_NAME"
        )
        
        if uploaded_objects_file is not None:
            try:
                # Use the unified file_to_list function
                input_file_list = file_to_list(uploaded_objects_file, uploaded_objects_file.name)
                
                if input_file_list:
                    st.success(f"✅ **File processed!** Found {len(input_file_list)} database objects")
                    with st.expander(f"🔍 Preview ({len(input_file_list)} items)"):
                        for i, obj in enumerate(input_file_list[:10]):
                            st.markdown(f"• `{obj}`")
                        if len(input_file_list) > 10:
                            st.markdown(f"... and {len(input_file_list) - 10} more")
                else:
                    st.warning("⚠️ No valid database objects found in file")
                    
            except Exception as e:
                st.error(f"❌ **Error processing file**: {str(e)}")
                input_file_list = []
    else:
        # Manual input option
        objects_input = st.text_area(
            "📦 Database Objects",
            placeholder="Enter database objects (one per line or comma-separated):\n\nExamples:\n• ACQ_P_CORE.SEN_COM_SLS_EQUIPMENT_HEALTH_REPORT\n• DWL_P_BASE.CUSTOMER_INFO\n• SCHEMA_NAME.TABLE_NAME",
            value="ACQ_P_CORE.SEN_COM_SLS_EQUIPMENT_HEALTH_REPORT",
            height=100,
            help="📝 **Format**: `SCHEMA.TABLE_NAME`\n📝 **Multiple Objects**: One per line or comma-separated\n🔍 **Examples**: ACQ_P_CORE.TABLE1, DWL_P_BASE.TABLE2",
            label_visibility="visible"
        )
        input_file_list = [x.strip() for x in objects_input.replace(',', '\n').split('\n') if x.strip()]
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Search Button and Results
    if st.button("🔍 **Start BTEQ Search**", type="primary", use_container_width=True):
        # Validation
        if not all([hostname, username, password, path]) or not input_file_list:
            st.error("❌ **Missing Information**: Please fill in all required fields")
            return
        
        if not input_file_list:
            st.error("❌ **No Objects**: Please provide at least one database object to search")
            return
        
        # Validate environment file for APP layer
        if layer == "APP" and uploaded_env_file is None:
            st.error("❌ **Environment File Required**: Please upload an environment file for APP layer")
            return
        
        # Show search progress with progress bar
        try:
            # Initialize progress tracking
            total_objects = len(input_file_list)
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Prepare for processing
            status_text.text(f"🔗 Establishing SSH connection...")
            
            # Setup similar to reveng function
            try:
                tables = input_file_list
            except: 
                tables = input_file_list

            # Database mapping dictionary (same as in reveng function)
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
            
            # Load environment file for APP layer
            if layer.lower() == 'app':
                import APP_ENV as env
                dic = env.read_env_file(uploaded_env_file, dic)
            
            # Initialize result dataframe
            import pandas as pd
            result_df = pd.DataFrame({'Table_name':[], 'bteqs':[]})
            
            # Create SSH connection
            import fabric
            ssh = fabric.Connection(
                host=hostname,
                port=port,
                user=username,
                connect_kwargs={'password': password}
            )
            
            # Process each object with progress updates
            for i, table in enumerate(tables):
                # Update progress
                progress = (i) / total_objects
                progress_bar.progress(progress)
                remaining = total_objects - i
                status_text.text(f"🔍 Processing: {table} | Remaining: {remaining}/{total_objects}")
                
                # Process the table using RE function
                btqs = RE_BTQ.RE(table, layer, dic, ssh, path)
                df = pd.DataFrame({'Table_name': table, 'bteqs': btqs})
                result_df = pd.concat([result_df, df], axis=0)
            
            # Complete progress
            progress_bar.progress(1.0)
            status_text.text(f"✅ Completed processing {total_objects} objects!")
            
            # Close SSH connection
            ssh.close()
            
            if result_df is not None and not result_df.empty:
                st.success(f"✅ **Search Complete!** Found {len(result_df)} BTEQ references")
                
                # Display results
                st.markdown("### 📄 BTEQ Search Results")
                st.markdown(f"📂 **Search Path**: `{path}`")
                st.markdown(f"🏧 **Layer**: {layer}")
                st.markdown(f"👤 **SSH User**: {username}")
                st.markdown(f"📋 **Objects Searched**: {len(input_file_list)}")
                
                # Show the results dataframe
                st.dataframe(
                    result_df,
                    use_container_width=True,
                    height=400
                )
                
                # Download button for results
                csv = result_df.to_csv(index=False)
                st.download_button(
                    label="💾 Download Results as CSV",
                    data=csv,
                    file_name=f"bteq_search_results_{layer.lower()}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
            else:
                st.warning("⚠️ **No Results**: No BTEQ files found for the specified objects")
                
        except Exception as e:
            st.error(f"❌ **Search Failed**: {str(e)}")
            st.error("Please check your SSH credentials and server connection.")

def view_analysis_ui():
    """Enhanced View Analysis UI with modern styling."""
    # Add custom CSS for this page
    st.markdown("""
        <style>
        /* Remove default spacing at top of page */
        .main .block-container {
            padding-top: 1rem !important;
        }
        .env-header {
            background: rgba(138, 43, 226, 0.05);
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #8a2be2;
            border: 1px solid rgba(138, 43, 226, 0.2);
            margin-bottom: 1rem;
        }
        .credentials-section {
            background: rgba(138, 43, 226, 0.05);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid rgba(138, 43, 226, 0.2);
            margin: 1rem 0;
        }
        .analysis-section {
            background: rgba(75, 0, 130, 0.05);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid rgba(75, 0, 130, 0.2);
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🔍 View Analysis Center")
    st.markdown("*Analyze database views and their dependencies across environments*")
    
    # Environment selection with enhanced styling
    st.markdown("""
        <div class="env-header" style="text-align: center; padding: 0rem;">
            <h3 style="margin: 0; color: #8a2be2;">🌍 Environment Selection</h3>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("Choose your target Teradata environment for view analysis")
    
    environment = st.segmented_control(
        label="🔍 Select Teradata Environment:",
        options=["qa", "prod", "dev"],
        format_func=lambda x: f"🟡 {x.upper()}" if x == "qa" else f"🔴 {x.upper()}" if x == "prod" else f"🟢 {x.upper()}",
        default="qa",
        selection_mode="single",
        help="ℹ️ **QA**: Testing environment | **PROD**: Production environment | **DEV**: Development environment"
    )
    
    # Enhanced environment info
    env_info = {
        "qa": {"color": "🟡", "desc": "Quality Assurance - Safe for testing", "host": "tdplqa.corp.pep.pvt"},
        "prod": {"color": "🔴", "desc": "Production - Live data environment", "host": "tdplprod.corp.pep.pvt"},
        "dev": {"color": "🟢", "desc": "Development - Experimental environment", "host": "tdpldev.corp.pep.pvt"}
    }
    
    st.success(f"{env_info[environment]['color']} **{environment.upper()} Environment Selected**\n\n📍 {env_info[environment]['desc']}\n🔗 Host: `{env_info[environment]['host']}`")
    
    # Enhanced Teradata Credentials section
    st.markdown("""
        <div class="credentials-section" style="text-align: center; padding: 0rem;">
            <h3 style="margin: 0;color: #8a2be2; ">🔐 Authentication Credentials</h3>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("🔒 *Secure login to access Teradata view information*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        td_username = st.text_input(
            "👤 Teradata User ID",
            placeholder="e.g., 12345678 or username",
            help="📝 **Employee ID Format**: 8-digit number (uses LDAP)\n📝 **Username Format**: Standard username (uses basic auth)",
            label_visibility="visible"
        )
    
    with col2:
        td_password = st.text_input(
            "🔑 Password",
            type="password",
            placeholder="Enter your secure password",
            help="🔒 Your Teradata account password - kept secure and encrypted",
            label_visibility="visible"
        )
    
    st.divider()
    
    # Enhanced View Input Section
    st.markdown("""
        <div class="analysis-section" style="text-align: center; padding: 0rem;">
            <h3 style="margin: 0; color: #4b0082;">📊 View Configuration</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Input method selection with segmented control
    view_input_method = st.segmented_control(
        "🔄 Select Input Method:",
        options=["Manual Input", "File Input"],
        default="Manual Input",
        help="📝 **Manual Input**: Type view names directly\n📁 **File Input**: Upload Excel/CSV/TXT file"
    )
    
    view_list = []
    if view_input_method == "File Input":
        # File upload option
        st.markdown("📁 **Upload file containing database view names**")
        uploaded_view_file = st.file_uploader(
            "📁 Choose File (Excel/CSV/TXT)",
            type=['xlsx', 'xls', 'csv', 'txt'],
            accept_multiple_files=False,
            help="📄 **Supported**: .xlsx, .xls, .csv, .txt\n📝 **Format**: One view name per row or comma-separated\n📈 **Example**: SCHEMA_NAME.VIEW_NAME"
        )
        
        if uploaded_view_file is not None:
            try:
                # Use the unified file_to_list function
                view_list = file_to_list(uploaded_view_file, uploaded_view_file.name)
                
                if view_list:
                    st.success(f"✅ **File processed!** Found {len(view_list)} view names")
                    with st.expander(f"🔍 Preview ({len(view_list)} items)"):
                        for i, view_name in enumerate(view_list[:10]):
                            st.markdown(f"• `{view_name}`")
                        if len(view_list) > 10:
                            st.markdown(f"... and {len(view_list) - 10} more")
                else:
                    st.warning("⚠️ No valid view names found in file")
                    
            except Exception as e:
                st.error(f"❌ **Error processing file**: {str(e)}")
                view_list = []
    else:
        # Manual input option
        view_input = st.text_area(
            "📆 Database Views",
            placeholder="Enter database view names (one per line or comma-separated):\n\nExamples:\n• DWL_P_BASE.V_CUSTOMER_INFO\n• ACQ_P_DIM.V_PRODUCT_HIERARCHY\n• SCHEMA_NAME.VIEW_NAME",
            value="DWL_P_BASE.V_CUSTOMER_INFO",
            height=100,
            help="📝 **Format**: `SCHEMA.VIEW_NAME`\n📝 **Multiple Views**: One per line or comma-separated\n🔍 **Auto-conversion**: Production names automatically converted for QA",
            label_visibility="visible"
        )
        view_list = [x.strip() for x in view_input.replace(',', '\n').split('\n') if x.strip()]
    
    # Auto-convert database names for QA environment
    if environment == 'qa' and view_list:
        st.markdown("#### 🔄 QA Environment Auto-Conversion")
        converted_view_list = []
        conversions_made = []
        
        for view_name in view_list:
            # Case-insensitive replacement of '_P_' with '_S1_'
            if '_p_' in view_name.lower():
                original_name = view_name
                import re
                converted_name = re.sub(r'_[pP]_', '_S1_', view_name)
                converted_view_list.append(converted_name)
                if converted_name != original_name:
                    conversions_made.append((original_name, converted_name))
            else:
                converted_view_list.append(view_name)
        
        if conversions_made:
            st.info("🔄 **Automatic Production → QA Conversion Applied**")
        else:
            st.success("✅ No conversion needed - views already in QA format")
            
        view_list = converted_view_list
    
    # Enhanced action button with validation
    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    
    with col_btn2:
        if st.button(
            "🚀 Start View Analysis", 
            type="primary", 
            use_container_width=True,
            help="Connect to Teradata and analyze view dependencies"
        ):
            if not view_list:
                st.error("⚠️ **Missing Views**: Please enter at least one database view name")
            elif not td_username:
                st.error("⚠️ **Missing User ID**: Please enter your Teradata User ID")
            elif not td_password:
                st.error("⚠️ **Missing Password**: Please enter your Teradata password")
            else:
                # Initialize progress tracking
                total_views = len(view_list)
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                teradata_connection = None
                try:
                    # Establish connection
                    status_text.text(f"🔗 Connecting to {environment.upper()} environment...")
                    teradata_connection = tb.sh.connect_teradata(
                        environment=environment, 
                        username=td_username, 
                        password=td_password
                    )
                    teradata_cursor = teradata_connection.cursor()
                    
                    # Convert to uppercase for consistency
                    view_list_upper = [view.upper() for view in view_list]
                    
                    # Process views with progress updates
                    status_text.text(f"🔍 Analyzing {total_views} views...")
                    progress_bar.progress(0.3)
                    
                    # Perform view analysis
                    view_analysis_df = va.views_analysis(view_list_upper, teradata_cursor)
                    
                    # Update progress
                    progress_bar.progress(0.8)
                    status_text.text(f"📊 Processing analysis results...")
                    
                    # Complete progress
                    progress_bar.progress(1.0)
                    status_text.text(f"✅ Analysis complete for {total_views} views!")
                    
                    if view_analysis_df is not None and not view_analysis_df.empty:
                        st.success(f"✅ **Analysis Complete!** Found {len(view_analysis_df)} view dependencies")
                        
                        # Display results
                        st.markdown("### 📊 View Analysis Results")
                        st.markdown(f"📂 **Environment**: {environment.upper()}")
                        st.markdown(f"👤 **User**: {td_username}")
                        st.markdown(f"📆 **Views Analyzed**: {len(view_list)}")
                        st.markdown(f"🔗 **Dependencies Found**: {len(view_analysis_df)}")
                        
                        # Show the results dataframe
                        st.dataframe(
                            view_analysis_df,
                            use_container_width=True,
                            height=400
                        )
                        
                        # Download button for results
                        csv = view_analysis_df.to_csv(index=False)
                        st.download_button(
                            label="💾 Download Analysis Results as CSV",
                            data=csv,
                            file_name=f"view_analysis_results_{environment}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                        
                    else:
                        st.warning("⚠️ **No Results**: No view dependencies found for the specified views")
                        
                except Exception as e:
                    st.error(f"❌ **Analysis Failed**: {str(e)}")
                    st.error("Please check your credentials and view names.")
                    
                finally:
                    # Always close the connection if it was established
                    if teradata_connection is not None:
                        try:
                            teradata_connection.close()
                            st.success("✅ Teradata connection closed successfully!")
                        except Exception as close_error:
                            st.warning(f"⚠️ Connection close warning: {str(close_error)}")


# ---- Utility Functions ----
def check_login(username, password):
    """Check login credentials."""
    return username == "admin" and password == "password"

# ---- Sidebar Navigation ----
def sidebar_navigation():
    """Sidebar navigation and tool selection."""
    st.sidebar.title("Navigation")
    if st.session_state.get("logged_in", False):
        page_options = {
            "Main Page": "main",
            "Search & Download Files": "search",
            "BTEQ Analysis": "bteq_analysis",
            "BTEQ Search": "bteq_search",
            "Table Schema Info": "tbl_info",
            "View Analysis": "view_analysis"
        }
        # When on download page, highlight "Search & Download Files" as active
        current_page = st.session_state.page
        if current_page == "download":
            current_page = "search"
        
        choice = st.sidebar.radio("Go to:", list(page_options.keys()),
                                  index=list(page_options.values()).index(current_page) if current_page in page_options.values() else 0)
        # Only navigate if user actually selected a different page (not if we're on download page)
        if st.session_state.page not in ["download"] and st.session_state.page != page_options[choice]:
            st.session_state.page = page_options[choice]
            st.rerun()
        elif st.session_state.page == "download" and page_options[choice] != "search":
            # If on download page and user selects something other than search, navigate there
            st.session_state.page = page_options[choice]
            st.rerun()
        st.sidebar.markdown("---")
        if st.sidebar.button("Logout"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.session_state.page = "login"
            st.session_state.logged_in = False
            st.rerun()
    else:
        st.sidebar.info("Please log in to access tools.")

# ---- Main App Routing ----
def main():
    """Main app logic and routing."""
    if "page" not in st.session_state:
        st.session_state.page = "login"
    sidebar_navigation()
    page = st.session_state.page
    if page == "login":
        login_ui()
    elif page == "main":
        main_ui()
    elif page == "tbl_info":
        tbl_info_ui()
    elif page == "bteq_analysis":
        bteq_analysis_ui()
    elif page == "bteq_search":
        bteq_search_ui()
    elif page == "view_analysis":
        view_analysis_ui()
    elif page == "search":
        search_ui()
    elif page == "download":
        download_ui()
    else:
        st.error("Unknown page. Resetting to main.")
        st.session_state.page = "main"
        st.rerun()

if __name__ == "__main__":
    main()

