import socket
import threading
import protocol
import Server_functions
#
# Server configuration
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 5555  # Port to listen on


# Function to handle each client connection
def handle_client(client_socket, address):
    print(f"Connection from {address} has been established.")

    while True:
        # Receive data from the client
        recived_dict  = protocol.get_message(client_socket)
        if recived_dict is None:
            break
        type_of_request = recived_dict["t"]
        print(recived_dict)
        response_dict = Server_functions.write_error("THIS DID NOT WORK")
        type_of_request = ""
        if type_of_request == "file from client to server":
            name_client, name_of_file, data_from_file = Server_functions.get_file_from_client(recived_dict)
            response_dict = Server_functions.send_ack_on_file_from_client()
        elif type_of_request == "ask for file from server":
            name_client, name_of_file = Server_functions.get_request_for_file(recived_dict)
            response_dict = Server_functions.send_file_to_user("server returnd file", b"this is the data")





        send_data = protocol.set_up_message(response_dict)
        client_socket.sendall(send_data)

    # Close the connection
    client_socket.close()
    print(f"Connection from {address} has been closed.")


# Main function for server
def main():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen(5)
    print(f"Server is listening on {HOST}:{PORT}")

    try:
        while True:
            # Accept a new connection
            client_socket, address = server_socket.accept()

            # Start a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.start()

    except KeyboardInterrupt:
        print("Server shutting down.")
        server_socket.close()


if __name__ == "__main__":
    main()
