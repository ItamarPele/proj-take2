def get_file_from_client(dict_from_clint):
    d = dict_from_clint
    name_of_client = d["n"]
    name_of_file = d["name_of_file"]
    binary_data_from_file = d["data_of_file"]
    return name_of_client, name_of_file, binary_data_from_file
