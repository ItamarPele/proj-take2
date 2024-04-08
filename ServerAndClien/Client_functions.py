def send_file_to_server(name, name_of_file, binary_data_in_file):
    return {
        "t": "file from client to server",
        "n": name,
        "name_of_file": name_of_file,
        "data_of_file": binary_data_in_file}


def ack(dict_from_server):
    ack_type = dict_from_server["specific ack type"]
    return ack_type
