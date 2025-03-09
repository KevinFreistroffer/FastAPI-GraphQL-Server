import bcrypt

def hash_password(password:str):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed

def verify_password(password: str, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)