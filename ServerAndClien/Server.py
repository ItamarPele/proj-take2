import socket
import threading
import protocol

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
        send_message = {"name":recived_dict["name"].upper()}
        send_data = protocol.set_up_message(send_message)
        # Echo the received data back to the client
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
