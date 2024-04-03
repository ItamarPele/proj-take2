import socket
import protocol
import Client_functions
# Server configuration
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5555  # The port used by the server


def main():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")
        while True:
            message = input("Enter message to send (type 'quit' to exit): ")
            send_dict  = Client_functions.send_server_file_to_save(message.encode(), "my name")
            if message.lower() == 'quit':
                break

            send_data = protocol.send_message(send_dict)
            client_socket.sendall(send_data)


            # Receive the echoed data from the server
            data = client_socket.recv(1024).decode()
            print(f"Received from server: {data}")

    except KeyboardInterrupt:
        print("\nClosing connection.")
    finally:
        # Close the connection
        client_socket.close()


if __name__ == "__main__":
    main()
