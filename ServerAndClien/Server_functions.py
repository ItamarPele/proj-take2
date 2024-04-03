def handle_message_and_return_response(dict):
    """
    :param dict with type of request and additional params
    :return: dict with response, sender_ip
    """
    type_of_request = dict["type"]
    # sender_ip = dict["sender_ip"]
    res = server_functions[type_of_request](dict)
    return res  # ,sender_ip


def recv_file_from_client(dict):
    """
    :param dict: dict with data
    :return: response if the files were succefully sent
    """
    data = dict["data"]
    print("DEBUG PRINT DATA ")
    print(data)
    # TODO
    # file is splited and added additional parts
    # each part is sent to a diffrent servent
    is_ok = True  # if worked
    error_message = "File was not transmited ok {more info}"  # if didn't work
    success_message = "file was received and saved successfully"  # if worked
    res_dict = {"is_ok": is_ok}
    if is_ok:
        res_dict.update({"message": success_message})
    else:
        res_dict.update({"message": error_message})
    return res_dict


def send_file_to_client(dict):
    """
    :param dict: dict with name of file, name of user,
    :return: dict with file or error message, is ok
    """
    name_of_file = dict["name_of_file"]
    name_of_user = dict["name_of_user"]
    # TODO
    # get file back and rebuilt
    data = b"test data"
    is_ok = True  # if worked
    error_message = "name of file was not found\ not enogh servents are on\ other erroe messages"  # if didn't work
    success_message = "file was received and saved successfully"  # if worked
    res_dict = {"is_ok": is_ok}
    if is_ok:
        res_dict.update({"message": success_message, "data": data})
    else:
        res_dict.update({"message": error_message})
    return res_dict


def ask_servernt_for_file(ip, name_of_file):
    """
    :param ip: ip of servent
    :param name_of_file: name of file asking for
    :return: part of file\error message
    """
    data = b"servent data test"
    return data


server_functions = {
    "recv_file_from_client": recv_file_from_client,
    "send_file_to_client": send_file_to_client
}
