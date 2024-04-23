import socket
import protocol
import Servent_functions

def servent():
    # Create a socket object
    servent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Get the local machine name
    host = socket.gethostname()
    port = 12345

    try:
        # Connect to super server
        servent_socket.connect((host, port))

        while True:
            # Receive request from super server
            data_dict = protocol.get_message()
            type_of_request = data_dict["t"]
            if type_of_request == "file from server to servant":
                name_of_file, data_in_file = Servent_functions.get_file_from_server(data_dict)
                #TODO
                #save data
                response_dict = Servent_functions.send_ack_on_file_from_server()






    except KeyboardInterrupt:
        print("server is not online\\troble connecting to server")
    finally:
        # Close the connection with super server
        servent_socket.close()

if __name__ == "__main__":
    servent()