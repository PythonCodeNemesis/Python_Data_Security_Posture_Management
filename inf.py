import requests

#file_path= "my_file.txt"
file_path= "my_confidential_file.txt"

file_data = open(file_path,'r').read()
print(file_data)

def upload_file(user_role, file_path):
  """Uploads a file to the doc storage."""
  file_data = open(file_path, 'r').read()
  payload = {
    "name" : file_path,
    "data" : file_data
  }
  headers = {'User-Role': user_role}
  response = requests.post('http://localhost:5000/upload', json=payload, headers=headers)
  assert response.status_code == 200

def get_file(user_role, file_path):
  """Gets a file from the doc storage."""
  headers = {'User-Role': user_role}
  response = requests.get('http://localhost:5000/get_file', params={'file_path': file_path, 'check_existence': True},
  headers=headers)
  if response.status_code == 200:
    new_downloaded_folder_path = "./downloads/"+file_path
    file_data = response.json()['file_data']
    open(new_downloaded_folder_path, 'w').write(file_data)
  else:
    print(f'File {file_path} does not exist.')

def set_access_control():
  """Sets the access control for a file."""
  user = 'user1'
  role = 'admin'
  permission = 'read'
  response = requests.post('http://localhost:5000/access_control', params={'file_path': file_path, 'user': user, 'role': role, 'permission': permission})
  assert response.status_code == 200

if __name__ == '__main__':
  upload_file(user_role="user", file_path="my_file.txt")
  upload_file(user_role="admin", file_path="my_file.txt")
  print("upload file done")
  get_file(user_role="admin", file_path="my_file.txt")
  print("get file function")

  # Perform requests with different access controls
  upload_file(user_role="admin", file_path="my_file.txt")                       # Uploaded successfully for admin
  upload_file(user_role="user", file_path="my_file.txt")                        # Uploaded successfully for user
  
  upload_file(user_role="admin", file_path="my_confidential_file.txt")                       # Uploaded successfully for admin
  upload_file(user_role="user", file_path="my_confidential_file.txt")  
  
  get_file(user_role="admin", file_path="my_file.txt")                        # Access granted for admin
  get_file(user_role="admin", file_path="my_confidential_file.txt")                           # Access granted for user

  get_file(user_role="user", file_path="my_confidential_file.txt")                           # Access granted for user

  # get_file('admin', 'file.txt')                          # Access granted for admin
  # get_file('user', 'file.txt')                           # Access denied for user


