import socket
import protocol
import client_protocol_functions
from encryption import AES, RSA

# Server configuration
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5555  # The port used by the server

IS_LOGGED_IN = False
NAME = None


def generate_and_share_aes_key_with_server(client_socket):
    """
    :return: agreed AES key
    """
    message = client_protocol_functions.request_rsa_key_from_server()
    send_data = protocol.set_up_and_encrypt_message(message, None)
    client_socket.sendall(send_data)
    data_dict = protocol.get_message(client_socket, None)

    assert data_dict["t"] == "rsa public key from server to client"
    rsa_key = client_protocol_functions.recv_rsa_public_key(data_dict)
    aes_key = AES.generate_key()
    encrypted_aes_key = RSA.encrypt_with_public_rsa_key(rsa_key, aes_key)
    message = client_protocol_functions.send_server_encrypted_aes_key(encrypted_aes_key)
    send_data = protocol.set_up_and_encrypt_message(message, None)
    client_socket.sendall(send_data)
    data_dict = protocol.get_message(client_socket, aes_key)
    assert data_dict["t"] == "ack"
    return aes_key


def login(client_socket: socket, aes_key: bytes, username: str, password: str):
    # TODO maybe add check that the username and password are ok
    message_to_server = client_protocol_functions.send_login_request_to_server(username, password)
    send_data = protocol.set_up_and_encrypt_message(message_to_server, aes_key)
    client_socket.sendall(send_data)
    data_dict = protocol.get_message(client_socket, aes_key)
    type_of_response = data_dict["t"]
    if type_of_response == "login ok":
        global IS_LOGGED_IN, NAME
        IS_LOGGED_IN = True
        NAME = username
        return True, "logged in"
    elif type_of_response == "error":
        error_type = client_protocol_functions.recv_error(data_dict)
        return False, f"did not log in: {error_type}"
    else:
        raise Exception("does not recognize response fom server")


def register(client_socket: socket, aes_key: bytes, username: str, password: str):
    # TODO maybe add check that the username and password are ok
    message_to_server = client_protocol_functions.send_registration_request_to_server(username, password)
    send_data = protocol.set_up_and_encrypt_message(message_to_server, aes_key)
    client_socket.sendall(send_data)
    data_dict = protocol.get_message(client_socket, aes_key)
    type_of_response = data_dict["t"]
    if type_of_response == "ack":
        return True, "registered successfully"
    elif type_of_response == "error":
        error_type = client_protocol_functions.recv_error(data_dict)
        return False, f"did not register: {error_type}"
    else:
        raise Exception("does not recognize response fom server")


def send_file_to_server(client_socket: socket, aes_key: bytes, username: str, file_name: str, file_info: bytes):
    message_to_server = client_protocol_functions.send_file_to_server(username, file_name, file_info)
    send_data = protocol.set_up_and_encrypt_message(message_to_server, aes_key)
    client_socket.sendall(send_data)
    data_dict = protocol.get_message(client_socket, aes_key)
    type_of_response = data_dict["t"]
    if type_of_response == "ack":
        return True, "file sent"
    elif type_of_response == "error":
        error_type = client_protocol_functions.recv_error(data_dict)
        return False, f"error from server: {error_type}"
    else:
        raise Exception("does not recognize response fom server")


def request_file_from_server(client_socket: socket, aes_key: bytes, username: str, file_name: str):
    message_to_server = client_protocol_functions.send_request_for_file(username, file_name)
    send_data = protocol.set_up_and_encrypt_message(message_to_server, aes_key)
    client_socket.sendall(send_data)
    data_dict = protocol.get_message(client_socket, aes_key)
    type_of_response = data_dict["t"]
    if type_of_response == "file from server to client":
        name_of_file, data_in_file = client_protocol_functions.get_file_from_server(data_dict)
        return True, (name_of_file, data_in_file)
    elif type_of_response == "error":
        error_type = client_protocol_functions.recv_error(data_dict)
        return False, f"error from server: {error_type}"
    else:
        raise Exception("does not recognize response fom server")


def request_file_names(client_socket: socket, aes_key: bytes, username: str):
    message_to_server = client_protocol_functions.send_request_for_file_names(username)
    send_data = protocol.set_up_and_encrypt_message(message_to_server, aes_key)
    client_socket.sendall(send_data)
    data_dict = protocol.get_message(client_socket, aes_key)
    type_of_response = data_dict["t"]
    if type_of_response == "send file names":
        file_names = client_protocol_functions.recv_file_names(data_dict) # kept in <list> type!
        return True, file_names
    elif type_of_response == "error":
        err_message = client_protocol_functions.recv_error(data_dict)
        return False, err_message
    else:
        raise Exception("does not recognize response fom server")









