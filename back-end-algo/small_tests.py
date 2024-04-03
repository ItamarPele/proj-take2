is_ok = True  # if worked
data = b"test"
error_message = "name of file was not found\ not enogh servents are on\ other erroe messages"  # if didn't work
success_message = "file was received and saved successfully"  # if worked
res_dict = {"is_ok": is_ok}
if is_ok:
    res_dict.update({"message": success_message, "data": data})
else:
    res_dict.update({"message": error_message})

print(res_dict)