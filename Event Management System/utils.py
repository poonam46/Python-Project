import os
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


