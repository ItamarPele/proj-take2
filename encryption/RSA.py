from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def generate_rsa_private_and_public_key():
    private_key = RSA.generate(2048)
    public_key = private_key.publickey().export_key()
    return private_key, public_key


def encrypt_with_public_rsa_key(public_rsa_key, message_in_bytes):
    object_public_key = RSA.import_key(public_rsa_key)
    cipher = PKCS1_OAEP.new(object_public_key)
    encrypted_message = cipher.encrypt(message_in_bytes)
    return encrypted_message


def dycript_with_private_rsa_key(private_key, encrypted_message):
    receiver_cipher = PKCS1_OAEP.new(private_key)
    decrypted_message = receiver_cipher.decrypt(encrypted_message)
    return decrypted_message
