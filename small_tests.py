import hashlib
import os

def hash_password(password):
    # Generate a random salt
    salt = os.urandom(16)

    # Hash the password with the salt
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), b"", 100000).hex()

    # Return the hashed password and salt
    return password_hash, b"".hex()


print(hash_password("o4l&opGVzvG%F3#Yzt2%*"))