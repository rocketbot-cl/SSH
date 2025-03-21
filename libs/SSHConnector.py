import paramiko
import json

class SSHConnector:
    def __init__(self):
        self.sessions = {}

    def connect_with_pem(self, hostname, publicKeyFile, username):
        """
        Establishes an SSH connection using a PEM key.
        """
        try:
            key = paramiko.RSAKey.from_private_key_file(publicKeyFile)
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=hostname, username=username, pkey=key)
            session_name = hostname  # Use hostname as a simple session name
            self.sessions[session_name] = client
            return f"SSH connection established with {hostname} using PEM. Session name: {session_name}"
        except Exception as e:
            return f"Error connecting with PEM: {e}"

    def connect_with_credentials(self, hostname, username, password):
        """
        Establishes an SSH connection using username and password.
        """
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=hostname, username=username, password=password)
            session_name = username + '@' + hostname  # Unique session name
            self.sessions[session_name] = client
            return f"SSH connection established with {hostname} using credentials. Session name: {session_name}"
        except Exception as e:
            return f"Error connecting with credentials: {e}"

    def create_folder(self, session_name, folderName):
        """
        Creates a folder on the remote server.
        """
        try:
            client = self.sessions.get(session_name)
            if not client:
                return f"No session found with name {session_name}"
            
            command = f"mkdir {folderName}"
            stdin, stdout, stderr = client.exec_command(command)
            err = stderr.read().decode().strip()
            if err:
                return f"Error creating folder: {err}"
            return f"Folder '{folderName}' created successfully on session {session_name}"
        except Exception as e:
            return f"Error creating folder: {e}"

    def change_directory(self, session_name, path_to_go):
        """
        Changes the current working directory on the remote server.
        """
        try:
            client = self.sessions.get(session_name)
            if not client:
                return f"No session found with name {session_name}"
            
            command = f"cd {path_to_go}"
            stdin, stdout, stderr = client.exec_command(command)
            err = stderr.read().decode().strip()
            if err:
                return f"Error changing directory: {err}"
            return f"Directory changed to '{path_to_go}' successfully on session {session_name}"
        except Exception as e:
            return f"Error changing directory: {e}"

    def execute_command(self, session_name, command_list_str):
        """
        Executes a command on the remote server.  The command should be a list.
        """
        try:
            client = self.sessions.get(session_name)
            if not client:
                return f"No session found with name {session_name}"
            
            # Safely evaluate the command string to a list
            try:
                command_list = json.loads(command_list_str)
                if not isinstance(command_list, list):
                    raise ValueError("Command must be a list")
                command = ' '.join(command_list)  # Convert list to string
            except json.JSONDecodeError:
                return "Invalid command format.  Must be a valid JSON list string (e.g., ['ls', '-l'])"
            except ValueError as ve:
                 return str(ve)


            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode().strip()
            err = stderr.read().decode().strip()
            if err:
                return f"Command executed with errors: {err}"
            return f"Command output: {output}"
        except Exception as e:
            return f"Error executing command: {e}"
        
    def write_in_file(self, session_name, pathToFile, textToWrite):
        """
        Writes text to a file on the remote server.
        """
        try:
            client = self.sessions.get(session_name)
            if not client:
                return f"No session found with name {session_name}"

            sftp = client.open_sftp()
            try:
                with sftp.open(pathToFile, 'w') as f:
                    f.write(textToWrite)
                return f"Successfully wrote to file: {pathToFile} on session {session_name}"
            except Exception as e:
                return f"Error writing to file: {e}"
            finally:
                sftp.close()
        except Exception as e:
            return f"Error opening SFTP session: {e}"

    def read_text_from_file(self, session_name, pathToFile):
        """
        Reads text from a file on the remote server.
        """
        try:
            client = self.sessions.get(session_name)
            if not client:
                return f"No session found with name {session_name}"

            sftp = client.open_sftp()
            try:
                with sftp.open(pathToFile, 'r') as f:
                    content = f.read().decode().strip()
                return f"Content of {pathToFile}: {content}"
            except Exception as e:
                return f"Error reading file: {e}"
            finally:
                sftp.close()
        except Exception as e:
            return f"Error opening SFTP session: {e}"
        
    def disconnect(self, session_name):
        """
        Closes the SSH connection.
        """
        try:
            client = self.sessions.get(session_name)
            if not client:
                return f"No session found with name {session_name}"

            client.close()
            del self.sessions[session_name]
            return f"SSH connection closed for session: {session_name}"
        except Exception as e:
            return f"Error disconnecting: {e}"