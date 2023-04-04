import hashlib
import os, string
from cryptography.fernet import Fernet

def to_bytes(s):
    return s.encode("utf-8")

def to_string(b):
    return b.decode("utf-8")

def encrypt(s, key):
    f = Fernet(to_bytes(key))
    return to_string(f.encrypt(to_bytes(s)))

def decrypt(s, key):
    f = Fernet(to_bytes(key))
    return to_string(f.decrypt(to_bytes(s)))

def hash_password(password, n=1):
    word = password
    for i in range(0,n):
        password_bytes = word.encode('utf-8')
        sha256 = hashlib.sha256()
        sha256.update(password_bytes)
        word = sha256.hexdigest()
    return word