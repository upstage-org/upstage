from cryptography.fernet import Fernet

cipher_key = Fernet.generate_key()
cipher = Fernet(cipher_key)

def encrypt(some_str):
    text = str.encode(some_str)
    return cipher.encrypt(text).decode()