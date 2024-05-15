from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def generate_key():
    return get_random_bytes(32)


def aes_encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = pad(plaintext.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    return ciphertext


def aes_decrypt(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = cipher.decrypt(ciphertext)
    plaintext = unpad(decrypted_data, AES.block_size)
    return plaintext.decode('utf-8')


if __name__ == "__main__":
    # Example usage:
    plaintext_message = "Hello, AES Encryption!"
    # Generate a random key
    encryption_key = generate_key()
    # Encrypt the message
    encrypted_message = aes_encrypt(plaintext_message, encryption_key)
    print(f"Encrypted Message: {encrypted_message}")

    # Decrypt the message
    decrypted_message = aes_decrypt(encrypted_message, encryption_key)
    print(f"Decrypted Message: {decrypted_message}")
