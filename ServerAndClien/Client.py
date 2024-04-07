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
        # Connect to the server
        client_socket.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")

        # Send data to the server
        while True:
            message = Client_functions.send_file_to_server("Itamar", "my_cool_file", b"this is the data in the file")
            #if message.lower() == 'quit':
                #break

            send_data = protocol.set_up_message(message)
            client_socket.sendall(send_data)

            # Receive the echoed data from the server
            data_dict = protocol.get_message(client_socket)

            print(f"Received from server: {data_dict}")

    except KeyboardInterrupt:
        print("\nClosing connection.")
    finally:
        # Close the connection
        client_socket.close()


if __name__ == "__main__":
    main()
