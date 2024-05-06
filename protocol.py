import msgpack

#
ZFILL_LENGTH = 5


def recvall(sock, size, debug_print=False):
    data = b''
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if debug_print:
            print(packet)
            print(len(packet))
            print(len(data) < size)
        if not packet:
            return None  # Connection closed prematurely
        data += packet
    return data


def set_up_message(dict_):
    message = b''
    packed_message = msgpack.packb(dict_)
    message += str(len(packed_message)).zfill(ZFILL_LENGTH).encode() + packed_message
    return message


def get_message(my_socket, debug_print=False):

    exit1 = False
    while not exit1:
        length = recvall(my_socket, ZFILL_LENGTH,True)
        if length is None:
            exit1 = False
        else:
            exit1 = True
    if debug_print:
        print("len " + str(length))
    decoded_len = length.decode()
    int_length = int(decoded_len)

    return msgpack.unpackb(recvall(my_socket, int_length))
