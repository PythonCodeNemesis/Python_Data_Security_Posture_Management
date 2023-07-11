import os
import re
from flask import Flask, request, jsonify
from cryptography.fernet import Fernet

app = Flask(__name__)

def data_discovery():
  """Discovers all sensitive data stored in the doc storage."""
  for root, directories, files in os.walk('.'):
    for file in files:
      file_path = os.path.join(root, file)
      if is_sensitive_data(file_path):
        print(f'{file_path} is sensitive data')

def is_sensitive_data(file_path):
  """Returns True if the given file path is sensitive data."""
  sensitive_data_patterns = ['.*PII.*', '.*confidential.*']
  for pattern in sensitive_data_patterns:
    if re.search(pattern, file_path):
      return True
  return False

def encrypt_file(file_path):
  """Encrypts the given file."""
  key = Fernet.generate_key()
  with open(file_path, 'rb') as file:
    file_data = file.read()
  encrypted_file_data = Fernet(key).encrypt(file_data)
  with open(file_path, 'wb') as file:
    file.write(encrypted_file_data)

def decrypt_file(file_path):
  """Decrypts the given file."""
  key = Fernet.generate_key()
  with open(file_path, 'rb') as file:
     encrypted_file_data = file.read()
  decrypted_file_data = Fernet(key).decrypt(encrypted_file_data)
  with open(file_path, 'wb') as file:
    file.write(decrypted_file_data)

@app.route('/upload', methods=['POST'])
def upload_file():
  """Uploads a file to the doc storage."""
  file = request.files['file']
  file_path = os.path.join('.', file.filename)
  if is_sensitive_data(file_path):
    encrypt_file(file_path)
  file.save(file_path)
  return 'File uploaded successfully'

@app.route('/get_file', methods=['GET'])
def get_file():
  """Gets a file from the doc storage."""
  file_path = request.args.get('file_path')
  if is_sensitive_data(file_path):
    decrypt_file(file_path)
  with open(file_path, 'rb') as file:
    file_data = file.read()
  return jsonify({'file_data': file_data})

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
