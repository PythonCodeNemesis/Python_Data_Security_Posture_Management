# Fernet module is imported from the 
# cryptography package
from cryptography.fernet import Fernet
  
# key is generated
key = Fernet.generate_key()
  
# value of key is assigned to a variable
f = Fernet(key)
  
# the plaintext is converted to ciphertext
file_path= "my_confidential_file.txt"
file_data = open(file_path,'rb').read()
print(file_data)
token = f.encrypt(file_data)
  
# display the ciphertext
print(token)
  
# decrypting the ciphertext
d = f.decrypt(token)
  
# display the plaintext
print(d)