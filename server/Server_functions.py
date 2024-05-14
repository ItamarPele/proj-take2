#
def get_file_from_client(dict_from_clint):
    d = dict_from_clint
    name_of_client = d["n"]
    name_of_file = d["name_of_file"]
    binary_data_from_file = d["data_of_file"]
    return name_of_client, name_of_file, binary_data_from_file


def send_ack_to_client(ack_type):
    return {"t": "ack", "specific_ack_type": ack_type}


def get_request_for_file(dict_from_clint):
    d = dict_from_clint
    name_of_client = d["n"]
    name_of_file = d["name_of_file"]
    ID = d["id"]
    return name_of_client, name_of_file, ID


def send_file_to_user(name_of_file, data_of_file):
    return {
        "t": "file from server to client",
        "name_of_file": name_of_file,
        "data_of_file": data_of_file
    }


def write_error(error_message):
    return {"t": "error", "error_message": error_message}


def send_file_to_servant(name_of_file, name_of_client, data_of_file, ID):
    return {
        "t": "file from server to servant",
        "name_of_file": name_of_file,
        "n": name_of_client,
        "data_of_file": data_of_file,
        "id": ID
    }


def recv_ack_from_servant(dict_from_servant):
    return dict_from_servant["specific_ack_type"]


def request_file_part(name_of_file, name_of_client, id):
    return {
        "t": "request file from servant",
        "name_of_file": name_of_file,
        "n": name_of_client,
        "id": id
    }


def recv_error_from_servant(dict_from_servant):
    error_message = dict_from_servant["error_message"]
    return error_message


def recv_file_part_from_servant(dict_from_servant):
    name_of_file = dict_from_servant["name_of_file"]
    data_of_file = dict_from_servant["data_of_file"]
    return name_of_file, data_of_file


def recv_request_to_be_servant(dict_from_servant):
    password = dict_from_servant["password"]
    return password


def send_ok_on_being_a_servant():
    return {"t": "ok on being a servant"}


def get_registration_from_client(dict_from_client):
    name_of_client = dict_from_client["n"]
    password = dict_from_client["password"]
    return name_of_client, password


def get_login_from_client(dict_from_client):
    name_of_client = dict_from_client["n"]
    password = dict_from_client["password"]
    return name_of_client, password


def send_login_ok():
    return {"t": "login ok"}

