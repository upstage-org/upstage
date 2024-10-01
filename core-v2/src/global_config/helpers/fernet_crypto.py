from cryptography.fernet import Fernet

from global_config import CIPHER_KEY

cipher = Fernet(CIPHER_KEY)


def encrypt(some_str):
    text = str.encode(some_str)
    return cipher.encrypt(text).decode()


def decrypt(some_enc_str):
    decrypted_text = cipher.decrypt(str.encode(some_enc_str))
    return decrypted_text.decode()
