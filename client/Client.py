import socket
import protocol
import Client_functions

# Server configuration
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5555  # The port used by the server


#
def main():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server
    client_socket.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")

    while True:
        message = Client_functions.send_file_to_server("Itamar", "my_cool_file", b"myfillllllllllllllll")

        send_data = protocol.set_up_message(message)
        client_socket.sendall(send_data)

        data_dict = protocol.get_message(client_socket,were_Am_I_from="Client")
        type_of_response = data_dict["t"]
        if type_of_response == "ack":
            ack_type = Client_functions.ack(data_dict)
            print(ack_type)
        if type_of_response == "file from server to client":
            name_of_file, data_in_file = Client_functions.get_file_from_server(data_dict)
            print(name_of_file, data_in_file)
        if type_of_response == "error":
            error_type = Client_functions.recv_error(data_dict)
            print(error_type)

        print(f"Received from server: {data_dict}")
        a = input()
        if a == 'q':
            break

    # Close the connection
    client_socket.close()


if __name__ == "__main__":
    main()
