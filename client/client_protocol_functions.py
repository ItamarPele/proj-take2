#
def send_file_to_server(name, name_of_file, binary_data_in_file):
    return {
        "t": "file from client to server",
        "n": name,
        "name_of_file": name_of_file,
        "data_of_file": binary_data_in_file}


def ack(dict_from_server):
    ack_type = dict_from_server["specific_ack_type"]
    return ack_type


def send_request_for_file(name, name_of_file):
    return {
        "t": "ask for file from server",
        "n": name,
        "name_of_file": name_of_file,
    }


def get_file_from_server(dict_from_server):
    d = dict_from_server
    name_of_file = d["name_of_file"]
    data_of_file = d["data_of_file"]
    return name_of_file, data_of_file


def recv_error(dict_from_server):
    error_message = dict_from_server["error_message"]
    return error_message


def send_registration_request_to_server(name, password):
    return {
        "t": "register",
        "n": name,
        "password": password
    }


def send_login_request_to_server(name, password):
    return {
        "t": "login",
        "n": name,
        "password": password
    }


def request_rsa_key_from_server():
    return {"t": "request rsa key"}


def recv_rsa_public_key(dict_from_server):
    return dict_from_server["rsa_key"]


def send_server_encrypted_aes_key(encrypted_aes_key):
    return {
        "t": "share aes key",
        "aes_key": encrypted_aes_key
    }


def send_request_for_file_names(username):
    return {
        "t": "client asks for file names",
        "n": username
    }


def recv_file_names(dict_from_server):
    file_names = dict_from_server["file_names"]
    return file_names
