from cryptography.fernet import Fernet
import json

PASSWORD_FILE = "passwords.json"

# Generate and secure encryption key
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("key.key", "rb").read()

# Password encryption
def encrypt_password(password):
    key = load_key()
    fernet = Fernet(key)
    return fernet.encrypt(password.encode())

def decrypt_password(encrypted_password):
    key = load_key()
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_password).decode()

# Save and retrieve passwords
def save_password(account, password):
    encrypted_password = encrypt_password(password)
    try:
        with open(PASSWORD_FILE, "r") as file:
            passwords = json.load(file)
    except FileNotFoundError:
        passwords = {}
    passwords[account] = encrypted_password.decode()
    with open(PASSWORD_FILE, "w") as file:
        json.dump(passwords, file)

def retrieve_password(account):
    try:
        with open(PASSWORD_FILE, "r") as file:
            passwords = json.load(file)
        encrypted_password = passwords.get(account)
        if encrypted_password:
            return decrypt_password(encrypted_password.encode())
        else:
            return "Account not found."
    except FileNotFoundError:
        return "No passwords saved."
