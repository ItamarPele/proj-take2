import socket
import protocol
import client_protocol_functions
from encryption import AES, RSA

# Server configuration
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5555  # The port used by the server

IS_LOGGED_IN = False


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


#
def main():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server
    client_socket.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")

    aes_key = generate_and_share_aes_key_with_server(client_socket)
    print(f"aes key is: {aes_key}")

    while True:
        message = client_protocol_functions.send_file_to_server("T", "this is the file test22sd", b"HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
        # message = client_protocol_functions.send_request_for_file("T", "this is the file test2")
        # message = client_protocol_functions.send_registration_request_to_server("T", "T")
        # message = client_protocol_functions.send_login_request_to_server("T", "T")

        send_data = protocol.set_up_and_encrypt_message(message, aes_key)
        client_socket.sendall(send_data)

        data_dict = protocol.get_message(client_socket, aes_key)
        type_of_response = data_dict["t"]
        if type_of_response == "ack":
            ack_type = client_protocol_functions.ack(data_dict)
            print(ack_type)
        elif type_of_response == "file from server to client":
            name_of_file, data_in_file = client_protocol_functions.get_file_from_server(data_dict)
            print(name_of_file, data_in_file)
        elif type_of_response == "error":
            error_type = client_protocol_functions.recv_error(data_dict)
            print(error_type)
        elif type_of_response == "login ok":
            global IS_LOGGED_IN
            IS_LOGGED_IN = True
            print("logged in")

        print(f"Received from server: {data_dict}")
        a = input()
        if a == 'q':
            break

    # Close the connection
    client_socket.close()


if __name__ == "__main__":
    main()
