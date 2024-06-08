def get_file_from_server(dict_from_server):
    name_of_file = dict_from_server["name_of_file"]
    name_of_client = dict_from_server["n"]
    data_of_file = dict_from_server["data_of_file"]
    ID = dict_from_server["id"]
    return name_of_file, name_of_client, data_of_file, ID


def send_ack_on_file_from_server():
    return {"t": "ack",
            "specific_ack_type": "ack on file from servant to server"}


def recv_request_for_file_part(dict_from_server):
    name_of_file = dict_from_server["name_of_file"]
    name_of_client = dict_from_server["n"]
    ID = dict_from_server["id"]
    return name_of_file, name_of_client, ID


def write_error_to_server(error_message):
    return {
        "t": "error",
        "error_message": error_message}


def send_file_part_to_server(name, data):
    return {
        "t": "file part from servant to server",
        "name_of_file": name,
        "data_of_file": data}


def send_request_to_be_servant(password):
    return {
        "t": "request to be servant",
        "password": password
    }


def recv_error(dict_from_server):
    error_message = dict_from_server["error_message"]
    return error_message


def request_rsa_key_from_server():
    return {"t": "request rsa key"}


def recv_rsa_public_key(dict_from_server):
    return dict_from_server["rsa_key"]


def send_server_encrypted_aes_key(encrypted_aes_key):
    return {
        "t": "share aes key",
        "aes_key": encrypted_aes_key
    }


def send_pong_to_server():
    return {"t": "pong"}


def revc_delete_request(dict_from_server):
    name_of_file = dict_from_server["name_of_file"]
    name_of_client = dict_from_server["n"]
    ID = dict_from_server["id"]
    return name_of_file, name_of_client, ID
