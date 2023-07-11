from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import logging

app = Flask(__name__)

# Generate encryption key
encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# Example user roles and access control
user_roles = {
    'admin': ['view_documents', 'upload_documents', 'delete_documents', 'view_logs'],
    'user': ['view_documents', 'upload_documents']
}

documents = []

# Example threat intelligence feeds
threat_intelligence = {
    'malicious_documents': ['virus.docx', 'malware.pdf']
}

@app.route('/')
def home():
    return 'Document Management System'

@app.route('/documents', methods=['GET'])
def view_documents():
    user_role = request.headers.get('User-Role')
    if 'view_documents' in user_roles.get(user_role, []):
        return jsonify(documents)
    else:
        return jsonify({'error': 'Access Denied'}), 403

@app.route('/documents', methods=['POST'])
def upload_document():
    user_role = request.headers.get('User-Role')

    # Check user role permissions
    if 'upload_documents' not in user_roles.get(user_role, []):
        return jsonify({'error': 'Access denied'}), 403

    # Retrieve the encrypted document name
    encrypted_document_name = request.form.get('name')
    if not encrypted_document_name:
        return jsonify({'error': 'No document name provided'}), 400

    # Decrypt the document name
    try:
        document_name = cipher_suite.decrypt(encrypted_document_name.encode()).decode()
    except InvalidToken:
        return jsonify({'error': 'Invalid document name'}), 400

    # Perform document upload logic
    documents.append(document_name)
    logging.info(f"User uploaded document: {document_name}")

    return jsonify({'message': 'Document uploaded successfully'}), 200


# @app.route('/documents', methods=['POST'])
# def upload_document():
#     user_role = request.headers.get('User-Role')
#     if 'upload_documents' in user_roles.get(user_role, []):
#         document_name = request.form.get('name')
#         if document_name:
#             # Encrypt the document name before storing
#             encrypted_document_name = cipher_suite.encrypt(document_name.encode()).decode()
#             documents.append(encrypted_document_name)

#             # Log the document upload
#             logging.info(f"User uploaded document: {document_name}")

#             return jsonify({'message': 'Document uploaded successfully'})
#         else:
#             return jsonify({'error': 'Invalid document name'}), 400
#     else:
        # return jsonify({'error': 'Access Denied'}), 403

@app.route('/documents/<string:document_name>', methods=['DELETE'])
def delete_document(document_name):
    user_role = request.headers.get('User-Role')
    if 'delete_documents' in user_roles.get(user_role, []):
        # Decrypt the document name for comparison
        decrypted_document_name = cipher_suite.decrypt(document_name.encode()).decode()

        if decrypted_document_name in documents:
            documents.remove(decrypted_document_name)

            # Log the document deletion
            logging.info(f"User deleted document: {decrypted_document_name}")

            return jsonify({'message': 'Document deleted successfully'})
        else:
            return jsonify({'error': 'Document not found'}), 404
    else:
        return jsonify({'error': 'Access Denied'}), 403

@app.route('/check_threats', methods=['POST'])
def check_threats():
    user_role = request.headers.get('User-Role')
    if 'view_documents' in user_roles.get(user_role, []):
        document_name = request.form.get('name')
        if document_name:
            # Decrypt the document name for threat intelligence check
            decrypted_document_name = cipher_suite.decrypt(document_name.encode()).decode()

            if decrypted_document_name in threat_intelligence['malicious_documents']:
                return jsonify({'threat': 'Malicious document detected'})

            return jsonify({'message': 'No threats detected'})
        else:
            return jsonify({'error': 'Invalid document name'}), 400
    else:
        return jsonify({'error': 'Access Denied'}), 403

# def check_threats():
#     user_role = request.headers.get('User-Role')
#     if 'view_documents' in user_roles.get(user_role, []):
#         document_name = request.form.get('name')
#         if document_name:
#             # Decrypt the document name for threat intelligence check
#             decrypted_document_name = cipher_suite.decrypt(document_name.encode()).decode()

#             if decrypted_document_name in threat_intelligence['malicious_documents']:
#                 return jsonify({'threat': 'Malicious document detected'})

#             return jsonify({'message': 'No threats detected'})
#         else:
#             return jsonify({'error': 'Invalid document name'}), 400
#     else:
#         return jsonify({'error': 'Access denied'}), 403

#     headers = {
#       'User-Role': user_role,
#       'Encryption-Key': encryption_key,
#     }
#     return jsonify({'message': 'Document uploaded successfully'})

if __name__ == '__main__':
    app.run(debug=True)
