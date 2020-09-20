import bcrypt

def hash_pw(plaintext_password):
    if isinstance(plaintext_password, str):
        return bcrypt.hashpw(bytes(plaintext_password, 'utf-8'), bcrypt.gensalt())

def check_pw(plaintext_password, db_password):
    if isinstance(plaintext_password, str):
        return bcrypt.checkpw(bytes(plaintext_password, 'utf-8'), db_password)