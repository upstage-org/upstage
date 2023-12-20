# -*- coding: iso8859-15 -*-
#!/usr/bin/python3
import sys,os
#import pdb;pdb.set_trace()                                                      

from cryptography.fernet import Fernet

if __name__ != '__main__':
    from config.settings import CIPHER_KEY
    #cipher_key = Fernet.generate_key()

    # Generate once, reuse.
    cipher_key = CIPHER_KEY

    cipher = Fernet(cipher_key)

def encrypt(some_str):
    text=str.encode(some_str)
    return cipher.encrypt(text).decode()
    
def decrypt(some_enc_str):
    decrypted_text = cipher.decrypt(str.encode(some_enc_str))
    return decrypted_text.decode()

def check_password(enc_key,password):
    return decrypt(enc_key) == password

if __name__ == '__main__':
    c = Fernet(b'Y9fzvL6bbiTqWumKfk7-phWutaPjK_HcdhIHGqQmSg0=')
    text=str.encode('12345678')
    print(c.encrypt(text).decode())
    # print("Copy-paste this key: {}".format(Fernet.generate_key()))
