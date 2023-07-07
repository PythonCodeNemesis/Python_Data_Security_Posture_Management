from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import logging

app = Flask(__name__)

# Generate encryption key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# Example user roles and access control
user_roles = {
    'admin': ['encrypt_data', 'decrypt_data', 'view_logs', 'manage_vulnerabilities'],
    'user': ['encrypt_data', 'decrypt_data']
}

@app.route('/')
def home():
    return 'Data Security Posture Management Example'

@app.route('/encrypt', methods=['POST'])
def encrypt():
    # Example of data encryption
    data = request.form.get('data')
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    encrypted_data = cipher_suite.encrypt(data.encode())

    # Example of logging sensitive actions
    logging.info(f"User encrypted data: {data}")

    return encrypted_data.decode()

@app.route('/decrypt', methods=['POST'])
def decrypt():
    # Example of data decryption
    encrypted_data = request.form.get('encrypted_data')
    if not encrypted_data:
        return jsonify({'error': 'No encrypted data provided'}), 400

    decrypted_data = cipher_suite.decrypt(encrypted_data.encode())

    # Example of logging sensitive actions
    logging.info(f"User decrypted data: {decrypted_data.decode()}")

    return decrypted_data.decode()

# Example threat intelligence feeds
threat_intelligence = {
    'malicious_ip': ['192.168.0.1', '10.0.0.2'],
    'malware_hash': ['a1b2c3d4e5', 'f6g7h8i9j10']
}

@app.route('/check_threats', methods=['POST'])
def check_threats():
    # Example of checking threats based on threat intelligence feeds
    data = request.form.get('data')
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Check for malicious IP
    if data in threat_intelligence['malicious_ip']:
        return jsonify({'threat': 'Malicious IP detected'})

    # Check for malware hash
    if data in threat_intelligence['malware_hash']:
        return jsonify({'threat': 'Malware hash detected'})

    return jsonify({'message': 'No threats detected'})

if __name__ == '__main__':
    app.run(debug=True)
