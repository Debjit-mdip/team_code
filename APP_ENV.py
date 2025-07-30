import re
def read_env_file(env_file_path,ENV_VAR):
    try:
        with open(env_file_path, "r") as file:
            for line in file:
                # Clean up the line and match the pattern
                line = line.strip()
                # The regex pattern was slightly off for the value part.
                # It should allow for more characters typical in environment variable values.
                match = re.match(r'export\s+([A-Z0-9_]+)=(.+)', line)
                if match:
                    key = match.group(1)
                    value = match.group(2)
                    # Remove any backslashes if they somehow appear in key or value
                    key = key.replace("\\", "")
                    value = value.replace("\\", "")
                    key = '${'+key+'}'
                    # Correctly add key-value pairs to the 'APP' dictionary
                    ENV_VAR['APP'][key] = value
            return ENV_VAR

    except FileNotFoundError:
        print(f"Error: The file {env_file_path} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def read_re_env_file(env_file_path,ENV_VAR):
    try:
        with open(env_file_path, "r") as file:
            for line in file:
                # Clean up the line and match the pattern
                line = line.strip()
                # The regex pattern was slightly off for the value part.
                # It should allow for more characters typical in environment variable values.
                match = re.match(r'export\s+([A-Z0-9_]+)=(.+)', line)
                if match:
                    key = match.group(1)
                    value = match.group(2)
                    # Remove any backslashes if they somehow appear in key or value
                    key = key.replace("\\", "")
                    value = value.replace("\\", "")
                    key,value = value,key
                    key = '${'+key+'}'
                    # Correctly add key-value pairs to the 'APP' dictionary
                    ENV_VAR['APP'][key] = value
            return ENV_VAR

    except FileNotFoundError:
        print(f"Error: The file {env_file_path} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
 