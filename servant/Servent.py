import socket
import protocol
import Servent_functions
import time
import random
import multiprocessing
import os

Password = 125351


def servent(directory_path):
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
            recived_dict = protocol.get_message(servant_socket)
            if recived_dict["t"] != "ok on being a servant":
                print("did not authinticate right, exiting")
                info_on_error = "no info why failed to authinticate"
                if recived_dict["t"] == "error":
                    info_on_error = Servent_functions.recv_error(recived_dict)
                raise Exception(info_on_error)
            print("registered as servernt")

            while True:
                # Receive request from the server
                data_dict = protocol.get_message(servant_socket)
                type_of_request = data_dict["t"]
                response_dict = Servent_functions.write_error_to_server("no type was found")
                if type_of_request == "file from server to servant":
                    name_of_file, name_of_client, data_in_file, ID = Servent_functions.get_file_from_server(data_dict)
                    print("data in file" + str(data_in_file))
                    file_path = directory_path + "\\" + str(ID)
                    with open(file_path, 'w') as file:
                        file.write(data_in_file)
                    response_dict = Servent_functions.send_ack_on_file_from_server()
                elif type_of_request == "request file from servant":
                    name_of_file, name_of_client, ID = Servent_functions.recv_request_for_file_part(data_dict)
                    file_path = directory_path + "\\" + str(ID)
                    if not os.path.exists(file_path):
                        response_dict = Servent_functions.write_error_to_server("file id was not found")
                    else:
                        with open(file_path, 'r') as file:
                            data_in_file = file.read()
                        response_dict = Servent_functions.send_file_part_to_server(name_of_file, data_in_file)
                send_data = protocol.set_up_message(response_dict)
                servant_socket.sendall(send_data)



        except (ConnectionRefusedError, ConnectionResetError):
            print("Connection to server lost. Attempting to reconnect...")
            time.sleep(3)  # Attempt to reconnect every 10 seconds

        finally:
            # Close the connection with super server
            servant_socket.close()


if __name__ == "__main__":
    # List of directory paths
    directory_paths = [
        r"C:\Users\itama\PycharmProjects\ProjREALNOWPLEASWORK\servant\servant_dir1",
        r"C:\Users\itama\PycharmProjects\ProjREALNOWPLEASWORK\servant\servant_dir2",
        r"C:\Users\itama\PycharmProjects\ProjREALNOWPLEASWORK\servant\servant_dir3",
        r"C:\Users\itama\PycharmProjects\ProjREALNOWPLEASWORK\servant\servant_dir4",
        r"C:\Users\itama\PycharmProjects\ProjREALNOWPLEASWORK\servant\servant_dir5"
    ]

    # Create a process for each directory path
    processes = []
    for directory_path in directory_paths:
        process = multiprocessing.Process(target=servent, args=(directory_path,))
        process.start()
        processes.append(process)

    # Wait for all processes to finish
    for process in processes:
        process.join()

    print("All processes completed.")