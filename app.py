from email import header
import os
import re
from flask import Flask, request, jsonify
from cryptography.fernet import Fernet

app = Flask(__name__)
# key is generated
key = Fernet.generate_key()
print(key)
  
# value of key is assigned to a variable
f = Fernet(key)

# Example user roles and access control
user_roles = {
    'admin': ['upload_documents', 'get_document'],
    'user': ['upload_documents']
}

base_encrypted_file_path = "./encrypted"

def data_discovery():
  """Discovers all sensitive data stored in the doc storage."""
  for root, directories, files in os.walk('.'):
    for file in files:
      file_path = os.path.join(root, file)
      if is_sensitive_data(file_path):
        print(f'{file_path} is sensitive data')

def is_sensitive_data(file_path):
  """Returns True if the given file path is sensitive data."""
  print("check-if-senstitive")
  sensitive_data_patterns = ['.*PII.*', '.*confidential.*']
  for pattern in sensitive_data_patterns:
    if re.search(pattern, file_path):
      return True
  return False

def encrypt_file(file_path):
    """Encrypts the given file."""
    with open(file_path, 'rb') as file:
        file_data = file.read()
        print("File data read as", file_data)
    encrypted_file_data = f.encrypt(file_data)
    print("encrypyted as tokyo : ",encrypted_file_data)
    with open(file_path, 'wb') as file:
        file.write(encrypted_file_data)

def decrypt_file(file_path):
    """Decrypts the given file."""
    file_path = "./encrypted/" + file_path
    with open(file_path, 'r') as file:
        encrypted_file_data = file.read()
        print("encrypted_file_data read as", encrypted_file_data)
    decrypted_file_data = f.decrypt(encrypted_file_data).decode('utf-8')
    print("decyrpted",decrypted_file_data)
    with open(file_path, 'w') as file:
        file.write(decrypted_file_data)

@app.route('/upload', methods=['POST'])
def upload_file():
  """Uploads a file to the doc storage."""
  user_role = request.headers.get('User-Role')
  if 'upload_documents' in user_roles.get(user_role, []):
    print(request.get_json())
    fileName = request.json["name"]
    fileContent = request.json["data"]
    if is_sensitive_data(fileName):
      encrypted_file_path = base_encrypted_file_path + "/" + fileName
      with open(encrypted_file_path,"w") as file:
        file.write(fileContent)
      encrypt_file(encrypted_file_path)
      print("Data encrypted as " + open(encrypted_file_path, 'r').read())
    return 'File uploaded successfully'
  else:
    return 'Access Denied'

@app.route('/get_file', methods=['GET'])
def get_file():
  """Gets a file from the doc storage."""
  user_role = request.headers.get('User-Role')
  if 'get_document' in user_roles.get(user_role, []):
    file_path = request.args.get('file_path')
    if is_sensitive_data(file_path):
      decrypt_file(file_path)
    print("Inside get_file function")
    file_data = open("./encrypted/" + file_path, 'r').read()
    print(file_data)
    return jsonify({'file_data': file_data})
  else:
    return jsonify({'error': 'Access Denied'}), 403

@app.route('/users', methods=['GET'])
def get_users():
  """Gets all users."""
  return jsonify({'users': ['user1', 'user2']})

@app.route('/roles', methods=['GET'])
def get_roles():
  """Gets all roles."""
  return jsonify({'roles': ['admin', 'user']})

@app.route('/permissions', methods=['GET'])
def get_permissions():
  """Gets all permissions."""
  return jsonify({'permissions': ['read', 'write', 'delete']})

@app.route('/access_control', methods=['POST'])
def set_access_control():
  """Sets the access control for a file."""
  file_path = request.args.get('file_path')
  user = request.args.get('user')
  role = request.args.get('role')
  permission = request.args.get('permission')
  return jsonify({'success': True})

if __name__ == '__main__':
  app.run(debug=True)
