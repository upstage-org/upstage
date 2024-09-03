from cryptography.fernet import Fernet

cipher_key = Fernet.generate_key()
cipher = Fernet(cipher_key)


def encrypt(some_str):
    text = str.encode(some_str)
    return cipher.encrypt(text).decode()


def decrypt(some_enc_str):
    decrypted_text = cipher.decrypt(str.encode(some_enc_str))
    return decrypted_text.decode()
