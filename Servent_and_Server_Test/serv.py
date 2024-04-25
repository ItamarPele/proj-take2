import socket
from protocol import set_up_message, get_message

def receive_file_from_manager(manager_socket):
    # Receive message
    message = get_message(manager_socket)
    if message['action'] == 'send_file':
        file_name = message['file_name']
        file_data = message['file_data']
        # Save the received file
        with open(file_name, 'wb') as file:
            file.write(file_data)
        # Send response
        response = {'status': 'success'}
        manager_socket.sendall(set_up_message(response))
        print(f"File '{file_name}' received and saved.")
    else:
        print("Invalid action.")

def send_file_to_manager(file_path, manager_socket):
    # Read the file
    with open(file_path, 'rb') as file:
        file_data = file.read()
    # Prepare message
    message = {'status': 'success', 'file_data': file_data}
    # Send message
    manager_socket.sendall(set_up_message(message))

def main():
    servant_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servant_socket.bind(('servant_ip', servant_port))  # Change 'servant_ip' and servant_port to actual values
    servant_socket.listen(1)

    manager_socket, _ = servant_socket.accept()

    # Example usage
    receive_file_from_manager(manager_socket)
    send_file_to_manager('file.txt', manager_socket)

    manager_socket.close()
    servant_socket.close()

if __name__ == "__main__":
    main()
