import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os

# Generate encryption key
def generate_key():
    key = base64.urlsafe_b64encode(os.urandom(32))
    return key

# Encrypt data
def encrypt_data(key, data):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    return iv + ciphertext

# Decrypt data
def decrypt_data(key, encrypted_data):
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    data = decryptor.update(ciphertext) + decryptor.finalize()
    return data

# Data classification
def classify_data(data):
    sensitive_keywords = ['password', 'confidential', 'secret']
    if any(keyword in data.lower() for keyword in sensitive_keywords):
        return 'Sensitive'
    else:
        return 'Non-sensitive'

# Secure coding practices - View documents
def view_documents(user_role):
    headers = {'User-Role': user_role}
    response = requests.get('http://127.0.0.1:5000/documents', headers=headers)
    print(f'Response for {user_role}: {response.text}')

# Secure coding practices - Upload document
def upload_document(user_role, document_name):
    headers = {'User-Role': user_role}
    encrypted_document_name = encrypt_data(encryption_key, document_name.encode())
    data = {'name': base64.b64encode(encrypted_document_name).decode()}
    response = requests.post('http://127.0.0.1:5000/documents', headers=headers, data=data)
    print(f'Response for {user_role}: {response.text}')

# Secure coding practices - Delete document
def delete_document(user_role, document_name):
    headers = {'User-Role': user_role}
    encrypted_document_name = encrypt_data(encryption_key, document_name.encode())
    response = requests.delete(f'http://127.0.0.1:5000/documents/{base64.b64encode(encrypted_document_name).decode()}', headers=headers)
    print(f'Response for {user_role}: {response.text}')

# Threat intelligence - Check threats
def check_threats(user_role, document_name):
    headers = {'User-Role': user_role}
    encrypted_document_name = encrypt_data(encryption_key, document_name.encode())
    data = {'name': base64.b64encode(encrypted_document_name).decode()}
    response = requests.post('http://127.0.0.1:5000/check_threats', headers=headers, data=data)
    print(f'Response for {user_role}: {response.text}')

# Example usage
if __name__ == '__main__':
    encryption_key = generate_key()

    # Perform secure coding practices
    view_documents('admin')                # Access granted for admin role
    upload_document('user', 'file.txt')     # Document uploaded successfully for user role
    delete_document('admin', 'file.txt')    # Document deleted successfully for admin role

    # Perform threat intelligence check
    check_threats('admin', 'virus.docx')    # Malicious document detected for admin role
    check_threats('user', 'file.txt')       # No threats detected for user role
