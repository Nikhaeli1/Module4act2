from cryptography.fernet import Fernet

# In production, store this KEY in an environment variable
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

def encrypt_data(value):
    return cipher.encrypt(value.encode()).decode()

def decrypt_data(token):
    return cipher.decrypt(token.encode()).decode()