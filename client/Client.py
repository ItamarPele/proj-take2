import socket
import protocol
import Client_functions

# Server configuration
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5555  # The port used by the server

IS_LOGGED_IN = False


#
def main():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server
    client_socket.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")

    while True:
        message = Client_functions.send_file_to_server("T", "this is the file test22", b"123")
        #message = Client_functions.send_request_for_file("T", "this is the file test2")
        #message = Client_functions.send_registration_request_to_server("T", "T")
        #message = Client_functions.send_login_request_to_server("T", "T")

        send_data = protocol.set_up_message(message)
        client_socket.sendall(send_data)

        data_dict = protocol.get_message(client_socket)
        type_of_response = data_dict["t"]
        if type_of_response == "ack":
            ack_type = Client_functions.ack(data_dict)
            print(ack_type)
        elif type_of_response == "file from server to client":
            name_of_file, data_in_file = Client_functions.get_file_from_server(data_dict)
            print(name_of_file, data_in_file)
        elif type_of_response == "error":
            error_type = Client_functions.recv_error(data_dict)
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
