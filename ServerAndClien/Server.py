import socket
import threading
import protocol
import Server_functions
# Server configuration
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 5555  # Port to listen on
ZFILL_LEN = 10


# Function to handle each client connection
def handle_client(client_socket, address):
    print(f"Connection from {address} has been established.")
    i = 20
    while True:
        recived_dict = protocol.get_message(client_socket)
        print("recived dict")
        print(recived_dict)

        if not recived_dict:
            break

        res_dict,t = Server_functions.handle_message_and_return_response(recived_dict)
        print("tttttttttttttttttttttttttttttttttttttttttttttttttt")
        print(t)
        res_data = protocol.send_message(res_dict)

        # Echo the received data back to the client
        client_socket.sendall(res_data)
        if i == 10:
            break
        i -=1

    # Close the connection
    client_socket.close()
    print(f"Connection from {address} has been closed.")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server is listening on {HOST}:{PORT}")

    while True:
        # Accept a new connection
        client_socket, address = server_socket.accept()


        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()


if __name__ == "__main__":
    main()
