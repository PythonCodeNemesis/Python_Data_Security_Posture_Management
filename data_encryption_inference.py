import requests
from cryptography.fernet import Fernet, InvalidToken


# Generate encryption key
key = b'Y_ySo_2sVHHUCqMaqEQc_tcM_31jZQlH2YLt69JH0TQ='
cipher_suite = Fernet(key)

# Function to send a GET request to the /documents endpoint
def view_documents(user_role):
    headers = {'User-Role': user_role}
    response = requests.get('http://127.0.0.1:5000/documents', headers=headers)
    print(f'Response for {user_role}: {response.text}')

# Function to send a POST request to the /documents endpoint
def upload_document(user_role, document_name):
    headers = {'User-Role': user_role}
    # Encrypt the document name before sending the request
    encrypted_document_name = cipher_suite.encrypt(document_name.encode()).decode()
    data = {'name': encrypted_document_name}
    response = requests.post('http://127.0.0.1:5000/documents', headers=headers, data=data)
    print(f'Response for {user_role}: {response.text}')

# Function to send a DELETE request to the /documents/<document_name> endpoint
def delete_document(user_role, document_name):
    headers = {'User-Role': user_role}
    # Encrypt the document name before sending the request
    encrypted_document_name = cipher_suite.encrypt(document_name.encode()).decode()
    response = requests.delete(f'http://127.0.0.1:5000/documents/{encrypted_document_name}', headers=headers)
    print(f'Response for {user_role}: {response.text}')

# Demonstrate secure coding practices and data encryption
view_documents('admin')                     # Access granted for admin role
upload_document('user', 'file.txt')          # Document uploaded successfully for user role
delete_document('admin', 'file.txt')         # Document deleted successfully for admin role
