import socket
import threading
import Server_functions
import protocol
import time
import sys

sys.path.append(r'C:\Users\itama\PycharmProjects\ProjREALNOWPLEASWORK\server\back_end_algo')
import file_to_files

N = 2
K = 2
Server_work_area_directory = r"C:\Users\itama\PycharmProjects\ProjREALNOWPLEASWORK\server\server_work_area"

# Server configuration
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 5555  # Port to listen on

# List of servant addresses should be equal in lenth to n+k
servant_addresses = [('127.0.0.1', 10001),
                     ('127.0.0.1', 10002),
                     ('127.0.0.1', 10003),
                     ('127.0.0.1', 10004)]


# Function to check servant availability
def check_servant_availability(servant_address):
    try:
        servant_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servant_socket.settimeout(1)  # Set a timeout for connection attempt
        servant_socket.connect(servant_address)
        servant_socket.close()
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False


# Define a global variable to hold the list of available servants
available_servants = []


# Function to establish connections to available servants
def connect_to_available_servants():
    global available_servants
    for address in servant_addresses:
        if check_servant_availability(address):
            available_servants.append(address)
    return available_servants


# Function to periodically check for servant availability
def check_servant_availability_periodic():
    global available_servants
    while True:
        available_servants = connect_to_available_servants()
        time.sleep(5)  # Check servant availability every 10 seconds
        print(available_servants)
        print(len(available_servants))


# Function to handle each client connection
def handle_client(client_socket, address):
    print(f"Connection from {address} has been established.")
    num_of_available_servants = len(available_servants)
    while True:
        # Receive data from the client
        received_dict = protocol.get_message(client_socket)
        if received_dict is None:
            break
        type_of_request = received_dict["t"]
        print(received_dict)
        response_dict = Server_functions.write_error("error in the server, no response was generated")
        if type_of_request == "file from client to server":
            name_client, name_of_file, data_from_file = Server_functions.get_file_from_client(received_dict)
            # check if possible to distribute:
            # check if data is ok
            print(data_from_file)
            print(len(data_from_file))
            is_data_ok, error_message_if_not = file_to_files.CheckData(data_from_file, N, K)
            if not is_data_ok:
                response_dict = Server_functions.write_error("data in file is not ok " + error_message_if_not)
            # check avalabilty of servents
            elif len(available_servants) != N + K:
                response_dict = Server_functions.write_error(
                    "not enough available servants at this time, please try again at a later time")
            # Send parts to servant servers
            else:
                points_of_data = file_to_files.data_to_points(N, K, data_from_file)
                for i in range(len(points_of_data)):
                    current_servent_socket = available_servants[i]
                    dict_to_servant = Server_functions.send_file_to_servant(name_of_file, name_client,
                                                                            points_of_data[i])
                    data_to_servant = protocol.set_up_message(dict_to_servant)
                    current_servent_socket.sendall(data_to_servant)
                    dict_from_servent = protocol.get_message(current_servent_socket)
                    print(dict_from_servent)
                response_dict = Server_functions.send_ack_on_file_from_client()


        elif type_of_request == "ask for file from server":
            name_client, name_of_file = Server_functions.get_request_for_file(received_dict)
            # Request file from servant servers
            # Aggregate file parts from servant servers
            file_data = b""
            for servant_socket in available_servants:
                print("a")
            response_dict = Server_functions.send_file_to_user(name_of_file, file_data)

        send_data = protocol.set_up_message(response_dict)
        client_socket.sendall(send_data)

    # Close the connection
    client_socket.close()
    print(f"Connection from {address} has been closed.")


# Main function for server
def main():
    try:
        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the address and port
        server_socket.bind((HOST, PORT))

        # Listen for incoming connections
        server_socket.listen(10)
        print(f"Server is listening on {HOST}:{PORT}")

        # Start the thread for periodic servant availability check
        servant_check_thread = threading.Thread(target=check_servant_availability_periodic)
        servant_check_thread.start()

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
