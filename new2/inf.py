import requests

#file_path= "my_file.txt"
file_path= "my_confidential_file.txt"

file_data = open(file_path,'r').read()
print(file_data)

def upload_file():
  """Uploads a file to the doc storage."""
  file_data = open(file_path, 'r').read()
  payload = {
    "name" : file_path,
    "data" : file_data
  }
  response = requests.post('http://localhost:5000/upload', json=payload)
  assert response.status_code == 200

def get_file():
  """Gets a file from the doc storage."""
  response = requests.get('http://localhost:5000/get_file', params={'file_path': file_path, 'check_existence': True})
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
  upload_file()
  print("upload file done")
  get_file()
  print("get file function")
  set_access_control()
  print("set access control")

