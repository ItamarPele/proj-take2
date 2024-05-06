import msgpack
#
ZFILL_LENGTH = 40


def recvall(sock, size):
    data = b''
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            return None  # Connection closed prematurely
        data += packet
    return data


def set_up_message(dict_):
    message = b''
    packed_message = msgpack.packb(dict_)
    message += str(len(packed_message)).zfill(ZFILL_LENGTH).encode() + packed_message
    return message


def get_message(my_socket):
    exit1 = False
    while not exit1:
        length = recvall(my_socket, ZFILL_LENGTH)
        if length is None:
            exit1 = False
        else:
            exit1 = True
    print("L")
    print(length)
    int_length = int(length.decode())
    return msgpack.unpackb(recvall(my_socket, int_length))