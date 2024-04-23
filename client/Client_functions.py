#
def send_file_to_server(name, name_of_file, binary_data_in_file):
    return {
        "t": "file from client to server",
        "n": name,
        "name_of_file": name_of_file,
        "data_of_file": binary_data_in_file}


def ack(dict_from_server):
    ack_type = dict_from_server["specific ack type"]
    return ack_type


def send_request_for_file(name, name_of_file):
    return {
        "t": "ask for file from server",
        "n": name,
        "name_of_file": name_of_file}


def get_file_from_server(dict_from_server):
    d = dict_from_server
    name_of_file = d["name_of_file"]
    data_of_file = d["data_of_file"]
    return name_of_file, data_of_file


def recv_error(dict_from_server):
    error_message = dict_from_server["error_message"]
    return error_message
