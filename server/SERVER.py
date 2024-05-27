import socket
import threading
import server_protocol_functions
import protocol
import sys
from back_end_algo import file_to_files
from db.db_manager import DatabaseManager
import hashlib
from encryption import AES, RSA

N = 5
K = 2
PATH_TO_DB = r"C:\Users\itama\PycharmProjects\ProjREALNOWPLEASWORK\server\db\my_db.sqlite3"
# Server_lists_clients_and_passwods_hash = {"itamar": "12345"}

# Server configuration
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 5555  # Port to listen on

password_hash_list = ["2440fac262df7114f5c756cb9d694b8597044b60102eaffc64062f056d8473c2"]

# Define a global variable to hold the list of available servants
available_servants = []

# RSA Keys
RSA_PRIVATE, RSA_PUBLIC = RSA.generate_rsa_private_and_public_key()


def remove_disconnected_servants():
    global available_servants
    # Create a copy of the available_servants list to avoid modifying the list while iterating
    servants_to_check = available_servants.copy()
    for current_servant_socket, aes_key in servants_to_check:
        try:
            send_message = server_protocol_functions.send_ping_to_servant()
            send_data = protocol.set_up_and_encrypt_message(send_message,aes_key)
            current_servant_socket.sendall(send_data)
            current_servant_socket.settimeout(2)
            response_dict = protocol.get_message(current_servant_socket, aes_key)
            current_servant_socket.settimeout(None)
            type_of_response = response_dict["t"]
            # Check if the response is valid
            if type_of_response != "pong":
                raise socket.error("Invalid response from servant")
        except (socket.error, socket.timeout):
            # If an error occurs or the timeout is reached, the servant is considered disconnected
            print(f"Servant {current_servant_socket.getpeername()} is disconnected. Removing from the list.")
            available_servants.remove((current_servant_socket, aes_key))
            # Close the socket connection
            current_servant_socket.close()


def send_file_parts_to_servants(points_of_data, name_of_file, name_client, ID):
    global available_servants
    if len(points_of_data) != len(available_servants):
        return False, "not servant number not equal to n + k"
    for i in range(len(points_of_data)):
        current_servent_socket, aes_key = available_servants[i]
        dict_to_servant = server_protocol_functions.send_file_to_servant(name_of_file, name_client,
                                                                         str(points_of_data[i]), ID)
        data_to_servant = protocol.set_up_and_encrypt_message(dict_to_servant, aes_key)
        current_servent_socket.sendall(data_to_servant)
        dict_from_servant = protocol.get_message(current_servent_socket, aes_key)

        if dict_from_servant["t"] != "ack":
            return False, "no ack recived"
    return True, "ok"


def request_file_parts_from_servants(name_of_file, name_of_client, ID):
    global available_servants
    global N
    if len(available_servants) < N:
        return False, "not servants available now"
    points_of_data = []
    for i in range(len(available_servants)):
        current_servant_socket, aes_key = available_servants[i]
        dict_to_servant = server_protocol_functions.request_file_part(name_of_file, name_of_client, ID)
        data_to_servant = protocol.set_up_and_encrypt_message(dict_to_servant, aes_key)
        current_servant_socket.sendall(data_to_servant)
        dict_from_servant = protocol.get_message(current_servant_socket, aes_key)
        if dict_from_servant["t"] == "error":
            err_message = server_protocol_functions.recv_error_from_servant(dict_from_servant)
            print(err_message)
        elif dict_from_servant["t"] != "file part from servant to server":
            return False, "unkown response from servant"
        else:
            name_of_file_from_servant, data_to_file = server_protocol_functions.recv_file_part_from_servant(
                dict_from_servant)
            points_of_data.append(data_to_file)
    if len(points_of_data) < N:
        return False, "some servants lost data and now it cannot be retreived"
    return True, points_of_data


# Function to handle each client connection
def handle_client(client_socket, address):
    global available_servants
    global PATH_TO_DB
    global N
    global K

    aes_key = None

    print(f"Connection from {address} has been established.")
    while True:
        # Receive data from the client
        received_dict = protocol.get_message(client_socket, aes_key)

        if received_dict is None:
            break
        type_of_request = received_dict["t"]
        response_dict = server_protocol_functions.write_error("error in the server, no response was generated")
        if type_of_request == "request to be servant":
            password = server_protocol_functions.recv_request_to_be_servant(received_dict)
            password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), b"", 100000).hex()
            is_password_ok = password_hash in password_hash_list
            if is_password_ok:
                available_servants.append((client_socket, aes_key))
                response_dict = server_protocol_functions.send_ok_on_being_a_servant()
            else:
                response_dict = server_protocol_functions.write_error("passwords were not compatable")
            send_data = protocol.set_up_and_encrypt_message(response_dict, aes_key)
            client_socket.sendall(send_data)
            if not is_password_ok:
                client_socket.close()
            return None
        elif type_of_request == "register":
            global PATH_TO_DB
            name_of_client, password = server_protocol_functions.get_registration_from_client(received_dict)
            with DatabaseManager(PATH_TO_DB) as db:
                if db.does_username_exist(name_of_client):
                    response_dict = server_protocol_functions.write_error("name already registered")
                else:
                    db.add_user(name_of_client, password)
                    response_dict = server_protocol_functions.send_ack_to_client("registered successfully")
        elif type_of_request == "login":
            name_of_client, password = server_protocol_functions.get_login_from_client(received_dict)
            with DatabaseManager(PATH_TO_DB) as db:
                if not db.does_username_exist(name_of_client):
                    response_dict = server_protocol_functions.write_error("name is not registered")
                elif not db.authenticate_user(name_of_client, password):
                    response_dict = server_protocol_functions.write_error("password incorrect")
                else:
                    response_dict = server_protocol_functions.send_login_ok()
        elif type_of_request == "file from client to server":
            remove_disconnected_servants()

            name_client, name_of_file, data_from_file = server_protocol_functions.get_file_from_client(received_dict)
            is_data_ok, error_message_if_not = file_to_files.CheckData(data_from_file, N, K)
            if not is_data_ok:
                response_dict = server_protocol_functions.write_error("data in file is not ok " + error_message_if_not)
            elif len(available_servants) != N + K:
                print(f"num of avalable servants {len(available_servants)}")
                print(f"n+k = {N + K}")
                response_dict = server_protocol_functions.write_error(
                    "not enough available servants at this time, please try again at a later time")
            # Send parts to servant servers
            else:
                points_of_data = file_to_files.data_to_points(N, K, data_from_file)
                # get id
                user_id = -1
                with DatabaseManager(PATH_TO_DB) as db:
                    user_id = db.get_user_id_by_username(name_client)
                    if db.check_if_user_file_alreadt_exists(user_id, name_of_file):
                        response_dict = server_protocol_functions.write_error(f"file name already exists for this user")
                    else:
                        # record the file on the db
                        file_id = db.add_file(name_of_file, N, str(len(data_from_file)), user_id)
                        # send the files and record on db record the file on the databse
                        did_send_to_serveants, error_message_if_not = send_file_parts_to_servants(points_of_data,
                                                                                                  name_of_file,
                                                                                                  name_client, file_id)
                        if did_send_to_serveants:
                            response_dict = server_protocol_functions.send_ack_to_client(f"file part recived")
                        else:
                            db.delete_file(file_id)
                            response_dict = server_protocol_functions.write_error("error message from servant "
                                                                                  + str(error_message_if_not))
        elif type_of_request == "ask for file from server":
            remove_disconnected_servants()

            name_client, name_of_file = server_protocol_functions.get_request_for_file(received_dict)
            if len(available_servants) < N:
                response_dict = server_protocol_functions.write_error(
                    "not enough available servants at this time, please try again at a later time")
            else:
                with DatabaseManager(PATH_TO_DB) as db:
                    user_id = db.get_user_id_by_username(name_client)
                    file_id = db.get_file_id_by_user_and_filename(name_client, name_of_file)
                    succes, file_name, n_of_file, len_of_file = db.get_file(file_id)
                    if not succes:
                        response_dict = server_protocol_functions.write_error("file does not exist")
                    else:
                        did_work, file_parts_or_err_message = request_file_parts_from_servants(
                            name_of_file=file_name, name_of_client=name_client, ID=file_id)
                        if not did_work:
                            err_message = file_parts_or_err_message
                            response_dict = server_protocol_functions.write_error(
                                "problem with servants " + str(err_message))
                        else:
                            file_parts = file_parts_or_err_message
                            file_data = file_to_files.points_to_data(int(n_of_file), file_parts, int(len_of_file))
                            response_dict = server_protocol_functions.send_file_to_user(name_of_file, file_data)
                            # print("file-data " + str(file_data))
        elif type_of_request == "request rsa key":
            global RSA_PUBLIC
            response_dict = server_protocol_functions.send_rsa_public_key(RSA_PUBLIC)
        elif type_of_request == "share aes key":

            encrypted_aes_key = server_protocol_functions.recv_encrypted_aes_key(received_dict)
            global RSA_PRIVATE
            aes_key = RSA.dycript_with_private_rsa_key(RSA_PRIVATE, encrypted_aes_key)
            response_dict = server_protocol_functions.send_ack_to_client("aes key shared succesfully")
        elif type_of_request == "client asks for file names":
            name_client = server_protocol_functions.recv_request_for_file_names(received_dict)
            with DatabaseManager(PATH_TO_DB) as db:
                if not db.does_username_exist(name_client):
                    response_dict = server_protocol_functions.write_error("no such name")
                else:
                    user_id = db.get_user_id_by_username(name_client)
                    file_names_and_id = db.get_user_files(user_id)
                    file_names = [t[1] for t in file_names_and_id]
                    response_dict = server_protocol_functions.send_file_names(file_names)

        send_data = protocol.set_up_and_encrypt_message(response_dict, aes_key)
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
