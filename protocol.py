import msgpack
from encryption import AES

#
ZFILL_LENGTH = 5


def recvall(sock, size):
    data = b''
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            return None  # Connection closed prematurely
        data += packet
    return data


def set_up_and_encrypt_message(dict_, aes_key):
    message = b''
    packed_message = msgpack.packb(dict_)
    if aes_key is not None:
        encrypted_message = AES.aes_encrypt(packed_message, aes_key)
        message += str(len(encrypted_message)).zfill(ZFILL_LENGTH).encode() + encrypted_message
        return message
    message += str(len(packed_message)).zfill(ZFILL_LENGTH).encode() + packed_message
    return message


def get_message(my_socket, aes_key):
    exit1 = False
    while not exit1:
        length = recvall(my_socket, ZFILL_LENGTH)
        if length is None:
            exit1 = False
        else:
            exit1 = True
    decoded_len = length.decode()
    int_length = int(decoded_len)
    if aes_key is not None:
        encrypted_data = recvall(my_socket, int_length)
        decrypted_data = AES.aes_decrypt(encrypted_data, aes_key)
        return msgpack.unpackb(decrypted_data)
    return msgpack.unpackb(recvall(my_socket, int_length))
