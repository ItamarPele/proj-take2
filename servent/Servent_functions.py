def get_file_from_server(dict_from_server):
    name_of_file = dict_from_server["name_of_file"]
    name_of_client = dict_from_server["n"]
    data_of_file = dict_from_server["data_of_file"]
    return name_of_file, name_of_client, data_of_file


def send_ack_on_file_from_server():
    return {"t": "ack", "specific_ack_type": "ack on file from servant to server"}




