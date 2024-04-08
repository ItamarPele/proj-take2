import socket
import protocol
import Client_functions
import os

# Server configuration
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5555  # The port used by the server
file_of_client_path = r"C:\Users\itama\PycharmProjects\ProjREALNOWPLEASWORK\back-end-algo\File_of_client"

#
def main():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server
    client_socket.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")

    while True:
        usr_input = input("do you want to send file or request file? s for send and r for request")
        if usr_input == "r":
            name = input("enter name")
            name_of_file = input("enter name of file")
            message = Client_functions.send_request_for_file(name, name_of_file)
        if usr_input == "s":
            path_to_file = input("enter full path to file")
            with open(path_to_file, 'rb') as read_file:
                data_from_file = read_file.read()
            name_of_file = input("enter name of file")
            name_of_user = input("enter name")
            message = Client_functions.send_file_to_server(name_of_user, name_of_file, data_from_file)

        send_data = protocol.set_up_message(message)
        client_socket.sendall(send_data)

        data_dict = protocol.get_message(client_socket)
        type_of_response = data_dict["t"]
        if type_of_response == "ack":
            ack_type = Client_functions.ack(data_dict)
            print(ack_type)
        if type_of_response == "file from server to client":
            name_of_file, data_in_file = Client_functions.get_file_from_server(data_dict)
            with open(os.path.join(file_of_client_path, name_of_file), 'wb') as write_file:
                write_file.write(data_in_file)
            print(name_of_file, data_in_file)
        if type_of_response == "error":
            error_type = Client_functions.recv_error(data_dict)
            print(error_type)

        a = input()
        if a == 'q':
            break

    # Close the connection
    client_socket.close()


if __name__ == "__main__":
    main()
