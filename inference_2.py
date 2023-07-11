import requests
from cryptography.fernet import Fernet
import base64
import os


# Declare encryption key
encryption_key = Fernet.generate_key()

# Function to encrypt data
def encrypt_data(key, data):
    f = Fernet(key)
    encrypted_data = f.encrypt(data)
    return encrypted_data

# Function to decrypt data
def decrypt_data(key, encrypted_data):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data

# Function to send a GET request to the /documents endpoint
def view_documents(user_role):
    headers = {
      'User-Role': user_role,
      'Encryption-Key': encryption_key,
    }
    response = requests.get('http://127.0.0.1:5000/documents', headers=headers)
    print(f'Response for {user_role}: {response.text}')

# Function to send a POST request to the /documents endpoint
def upload_document(user_role, document_name):
    headers = {
      'User-Role': user_role,
      'Encryption-Key': encryption_key,
    }
    encrypted_document_name = encrypt_data(encryption_key, document_name.encode())
    data = {'name': encrypted_document_name}
    response = requests.post('http://127.0.0.1:5000/documents', headers=headers, data=data)
    print(f'Response for {user_role}: {response.text}')

# Function to send a DELETE request to the /documents/<document_name> endpoint
def delete_document(user_role, document_name):
    headers = {
      'User-Role': user_role,
      'Encryption-Key': encryption_key,
    }
    response = requests.delete(f'http://127.0.0.1:5000/documents/{document_name}', headers=headers)
    print(f'Response for {user_role}: {response.text}')

# Demonstrate secure coding practices
view_documents('admin')                # Access granted for admin role
upload_document('user', 'file.txt')     # Document uploaded successfully for user role
delete_document('admin', 'file.txt')    # Document deleted successfully for admin role
