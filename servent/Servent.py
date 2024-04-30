import socket
import protocol
import Servent_functions
import time

def servent():
    while True:
        # Create a socket object
        servant_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Get the local machine name
        host = "127.0.0.1"
        port = 5555

        try:
            # Connect to the server
            servant_socket.connect((host, port))
            print("Connected to server")

            while True:
                # Receive request from the server
                data_dict = protocol.get_message(servant_socket)
                type_of_request = data_dict["t"]
                if type_of_request == "file from server to servant":
                    name_of_file, data_in_file = Servent_functions.get_file_from_server(data_dict)
                    #TODO
                    #save data
                    response_dict = Servent_functions.send_ack_on_file_from_server()

        except (ConnectionRefusedError, ConnectionResetError):
            print("Connection to server lost. Attempting to reconnect...")
            time.sleep(10)  # Attempt to reconnect every 10 seconds

        finally:
            # Close the connection with super server
            servant_socket.close()

if __name__ == "__main__":
    servent()


if __name__ == "__main__":
    servent()