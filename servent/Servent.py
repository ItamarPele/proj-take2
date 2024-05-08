import socket
import protocol
import Servent_functions
import time
import random

Password = 125351

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
            request_dict = Servent_functions.send_request_to_be_servant(password=Password)
            data_to_send = protocol.set_up_message(request_dict)
            servant_socket.sendall(data_to_send)
            recived_dict = protocol.get_message(servant_socket,were_Am_I_from="start of declaring I am sock")
            if recived_dict["t"] != "ok on being a servant":
                print("did not authinticate right, exiting")
                info_on_error = "no info why failed to authinticate"
                if recived_dict["t"] == "error":
                    info_on_error = Servent_functions.recv_error(recived_dict)
                raise Exception(info_on_error)
            print("registered as servernt")



            while True:
                # Receive request from the server
                data_dict = protocol.get_message(servant_socket,were_Am_I_from="while true of servant")
                type_of_request = data_dict["t"]
                response_dict = Servent_functions.write_error_to_server("no type was found")
                if type_of_request == "file from server to servant":
                    name_of_file, name_of_client, data_in_file = Servent_functions.get_file_from_server(data_dict)
                    print("data n file" + str(data_in_file))
                    #TODO
                    #save data
                    response_dict = Servent_functions.send_ack_on_file_from_server()
                    send_data = protocol.set_up_message(response_dict)
                    print("send data" + str(send_data))
                    servant_socket.sendall(send_data)


        except (ConnectionRefusedError, ConnectionResetError):
            print("Connection to server lost. Attempting to reconnect...")
            time.sleep(3)  # Attempt to reconnect every 10 seconds

        finally:
            # Close the connection with super server
            servant_socket.close()


if __name__ == "__main__":
    servent()

