import paramiko
import fabric
import teradatasql
import json
import os
import streamlit as st
# os.chdir('c:/Users/2122693/OneDrive - Cognizant/NewApps2025/codes/d&a/')
# print(os.getcwd())
config_file='config_secrets.json'
def connect_ssh_server(user_nm,config_file=config_file):
    try:
        # Load server details from the config file
        with open(config_file, 'r') as file:
            config = json.load(file)
        
        print(user_nm)
        ssh_config = config[user_nm]
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        hostname = ssh_config['hostname']
        port = ssh_config['port']
        username = ssh_config['username']
        password = ssh_config['password']
        
        ssh.connect(hostname=hostname, port=port, username=username, password=password)
        sftp = ssh.open_sftp()
        
        st.success("SSH connection successful!")
        return ssh, sftp
    except paramiko.AuthenticationException:
        st.error("Authentication failed, please verify your credentials.")
    except paramiko.SSHException as sshException:
        st.error(f"Unable to establish SSH connection: {sshException}")
    except Exception as e:
        st.error(f"Operation error: {e}")

def connect_ssh(user_nm,config_file=config_file):
    try:
        # Load server details from the config file
        with open(config_file, 'r') as file:
            config = json.load(file)
    except: pass

        # print(user_nm)
    ssh_config = config[user_nm]
    hostname = ssh_config['hostname']
    port = ssh_config['port']
    username = ssh_config['username']
    password = ssh_config['password']
    try:
        # Establish SSH connection using Fabric
        conn = fabric.Connection(
            host=hostname,
            port=port,
            user=username,
            connect_kwargs={'password': password}
        )
        
        st.success("SSH connection successful!")
        return conn
    except Exception as e:
        st.error(f"Operation error: {e}")

def connect_teradata(environment='qa', username=None, password=None, config_file=config_file):
    try:
        # Load Teradata details from the config file
        with open(config_file, 'r') as file:
            config = json.load(file)
    except Exception as e:
        print(f"{e}")
        exit(0)

    # Get environment-specific configuration
    if environment not in config['teradata']:
        st.error(f"Environment '{environment}' not found in configuration")
        exit(0)
        
    teradata_config = config['teradata'][environment]
    
    hostname = teradata_config['host']
    
    # Username and password are now required since they're not in config
    if username is None or password is None:
        st.error("Username and password are required for Teradata connection")
        exit(0)
    
    # Check if username is 8-digit employee ID (requires LDAP)
    use_ldap = username.isdigit() and len(username) == 8
    
    try:
        if use_ldap:
            logmech = teradata_config['logmech']
            st.info(f"Connecting to Teradata {environment.upper()} environment using LDAP authentication...")
            teradata_connection = teradatasql.connect(host=hostname, user=username, password=password, logmech=logmech)
        else:
            st.info(f"Connecting to Teradata {environment.upper()} environment using standard authentication...")
            teradata_connection = teradatasql.connect(host=hostname, user=username, password=password)
        
        # teradata_cursor = teradata_connection.cursor()
        auth_type = "LDAP" if use_ldap else "Standard"
        st.success(f"Teradata {environment.upper()} connection successful using {auth_type} authentication!")

        return teradata_connection
    except Exception as e:
        st.error(f"Failed to connect to {environment.upper()}: {e}")
        exit(0)

# ssh, sftp = connect_ssh_server()
# conn = connect_ssh_server()
# teradata_conn = connect_teradata()