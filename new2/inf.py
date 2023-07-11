import requests

file_path= "my_file.txt"


file_data = open(file_path,'r').read()
print(file_data)

def upload_file():
  """Uploads a file to the doc storage."""
  file_data = open(file_path, 'r').read()
  print(file_data)
  response = requests.post('http://localhost:5000/upload', files={'file': file_data})
  assert response.status_code == 200

def get_file():
  """Gets a file from the doc storage."""
  response = requests.get('http://localhost:5000/get_file', params={'file_path': file_path, 'check_existence': True})
  if response.status_code == 200:
    file_data = response.json()['file_data']
    open(file_path, 'wb').write(file_data)
  else:
    print(f'File {file_path} does not exist.')

# def set_access_control():
#   """Sets the access control for a file."""
#   user = 'user1'
#   role = 'admin'
#   permission = 'read'
#   response = requests.post('http://localhost:5000/access_control', params={'file_path': file_path, 'user': user, 'role': role, 'permission': permission})
#   assert response.status_code == 200

if __name__ == '__main__':
  upload_file()
  get_file()
  # set_access_control()

upload_file()