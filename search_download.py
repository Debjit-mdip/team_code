import pandas as pd
import re
import os
import paramiko

def search_files(path, username, tptfile, hostname, port, password):
    # Create SSH connection using paramiko directly
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname=hostname, port=port, username=username, password=password)
    except paramiko.ssh_exception.AuthenticationException:
        raise Exception(f"❌ **Authentication Failed**: Invalid credentials for user '{username}' on {hostname}:{port}\n\n🔍 **Please check:**\n• Username is correct\n• Password is correct\n• Account is not locked")
    except paramiko.ssh_exception.NoValidConnectionsError:
        raise Exception(f"❌ **Connection Failed**: Unable to connect to {hostname}:{port}\n\n🔍 **Please check:**\n• Hostname/IP address is correct\n• Port {port} is accessible\n• Network connectivity")
    except paramiko.ssh_exception.SSHException as e:
        raise Exception(f"❌ **SSH Error**: {str(e)}\n\n🔍 **Please check your SSH server configuration**")
    except Exception as e:
        raise Exception(f"❌ **Connection Error**: {str(e)}\n\n🔍 **Please verify your connection details**")
    
    command = f"""
    pwd && find {path} -type f -iname '*{tptfile}*' -exec stat --format '%n %s %y' {{}} + | awk '{{printf "%s %s %s %.5fMB %s \\n", $3, $4, $5, $2/(1024*1024), $1}}'
    """
    
    # Execute command using paramiko
    stdin, stdout, stderr = ssh.exec_command(command)
    out = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    
    # Find all matches that do not include "BKP_" and any numbers followed by ".gz"
    outMatch = re.compile(rf"^(?!.*BKP_).*{tptfile}(?!.*\d+\.gz).*", re.IGNORECASE | re.MULTILINE).findall(out)
    # Remove the path from each line
    outMatch = [re.sub(rf"{path}", '', line) for line in outMatch]
    outMatch.sort(reverse=True)
    max_val = 10
    # [print(x) for i,x in enumerate(outMatch) if i<max_val]
    output_list=[]
    for x in outMatch:
        time,size,fname=x.rsplit(maxsplit=2)
        output_list.append([time,size,fname])
    # Create DataFrame
    out_df = pd.DataFrame(output_list, columns=['TimeStamp','Size','Filename'])
    ssh.close()
    return out_df
    
def download_files(path, username, localpath, file_list, hostname, port, password, progress_callback=None, status_callback=None):
    # local path
    if not os.path.exists(localpath):
        os.makedirs(localpath)
    faultyFiles = []
    
    # Create SSH connection using provided credentials
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname=hostname, port=port, username=username, password=password)
        sftp = ssh.open_sftp()
    except paramiko.ssh_exception.AuthenticationException:
        raise Exception(f"❌ **Authentication Failed**: Invalid credentials for user '{username}' on {hostname}:{port}\n\n🔍 **Please check:**\n• Username is correct\n• Password is correct\n• Account is not locked")
    except paramiko.ssh_exception.NoValidConnectionsError:
        raise Exception(f"❌ **Connection Failed**: Unable to connect to {hostname}:{port}\n\n🔍 **Please check:**\n• Hostname/IP address is correct\n• Port {port} is accessible\n• Network connectivity")
    except paramiko.ssh_exception.SSHException as e:
        raise Exception(f"❌ **SSH Error**: {str(e)}\n\n🔍 **Please check your SSH server configuration**")
    except Exception as e:
        raise Exception(f"❌ **Connection Error**: {str(e)}\n\n🔍 **Please verify your connection details**")
    
    file_len = len(file_list)
    for index, datafile in enumerate(file_list):
        file = path + datafile
        local_file = os.path.join(localpath, datafile)
        if status_callback:
            status_callback(f"Downloading {datafile}...\n Remaining {file_len-index-1}")
        try:
            file_size = sftp.stat(file).st_size
            def callback(transferred, total):
                if progress_callback:
                    progress_callback(transferred, total)
            sftp.get(file, local_file, callback=callback)
            if status_callback:
                status_callback(f"{datafile} downloaded successfully!")
        except Exception as e:
            faultyFiles.append(datafile)
            if status_callback:
                status_callback(f"Error downloading {datafile}: {e}")
    sftp.close()
    ssh.close()
    return faultyFiles