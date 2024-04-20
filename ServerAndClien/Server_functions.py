#
def get_file_from_client(dict_from_clint):
    d = dict_from_clint
    name_of_client = d["n"]
    name_of_file = d["name_of_file"]
    binary_data_from_file = d["data_of_file"]
    return name_of_client, name_of_file, binary_data_from_file


def send_ack_on_file_from_client():
    return {"t": "ack", "specific ack type": "ack on file from sever to client"}


def get_request_for_file(dict_from_clint):
    d = dict_from_clint
    name_of_client = d["n"]
    name_of_file = d["name_of_file"]
    return name_of_client, name_of_file


def send_file_to_user(name_of_file, data_of_file):
    return {
        "t": "file from server to client",
        "name_of_file": name_of_file,
        "data_of_file": data_of_file
    }


def write_error(error_message):
    return {"t": "error", "error message": error_message}

