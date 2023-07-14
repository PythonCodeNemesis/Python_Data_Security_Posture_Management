import requests

base_url = 'http://localhost:5000'

def upload_file(user, file_path):
    """Uploads a file to the document storage."""
    file_data = open(file_path, 'r').read()
    payload = {
        "name": file_path,
        "data": file_data
    }
    response = requests.post(f'{base_url}/upload', json=payload)
    if response.status_code == 200:
        print(f'File {file_path} uploaded successfully for user {user}')
    else:
        print(f'Error uploading file {file_path} for user {user}')

def get_file(user, file_path):
    """Gets a file from the document storage."""
    response = requests.get(f'{base_url}/get_file', params={'file_path': file_path})
    if response.status_code == 200:
        file_data = response.json()['file_data']
        print(f'File content for user {user}: {file_data}')
    else:
        print(f'Error retrieving file {file_path} for user {user}')

def set_access_control(user, file_path, role, permission):
    """Sets the access control for a file."""
    response = requests.post(f'{base_url}/access_control', params={'file_path': file_path, 'user': user, 'role': role, 'permission': permission})
    if response.status_code == 200:
        print(f'Access control set successfully for user {user} on file {file_path}')
    else:
        print(f'Error setting access control for user {user} on file {file_path}')

if __name__ == '__main__':
    encryption_key = 'your_encryption_key'

    # Perform requests with different access controls
    upload_file('admin', 'file.txt')                       # Uploaded successfully for admin
    upload_file('user', 'file.txt')                        # Uploaded successfully for user

    set_access_control('admin', 'file.txt', 'admin', 'write')    # Access control set for admin
    set_access_control('user', 'file.txt', 'user', 'read')       # Access control set for user

    get_file('admin', 'file.txt')                          # Access granted for admin
    get_file('user', 'file.txt')                           # Access granted for user

    set_access_control('admin', 'file.txt', 'user', 'read')       # Access control changed for admin

    get_file('admin', 'file.txt')                          # Access granted for admin
    get_file('user', 'file.txt')                           # Access denied for user
