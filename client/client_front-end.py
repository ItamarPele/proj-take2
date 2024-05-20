import tkinter as tk
from tkinter import messagebox, filedialog
import socket
from ttkthemes import ThemedStyle

# Import the necessary functions from the client_functions file
from client.client_functions import generate_and_share_aes_key_with_server, login, register, send_file_to_server, request_file_from_server


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Authentication App")
        self.geometry("500x400")

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 5555))
        self.aes_key = generate_and_share_aes_key_with_server(self.client_socket)

        self.configure_styles()

        # Create the login/registration page
        self.login_page = LoginPage(self)
        self.login_page.pack(fill="both", expand=True)

    def configure_styles(self):
        # Configure the theme
        self.style = ThemedStyle(self)
        self.style.set_theme("clearlooks")

    def show_file_management_page(self, username):
        self.login_page.pack_forget()
        self.file_management_page = FileManagementPage(self, username)
        self.file_management_page.pack(fill="both", expand=True)


class LoginPage(tk.ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the input fields
        input_frame = tk.ttk.Frame(self, padding=20)
        input_frame.pack(fill="both", expand=True)

        # Username label and entry
        username_label = tk.ttk.Label(input_frame, text="Username:")
        username_label.pack()
        self.username_entry = tk.ttk.Entry(input_frame)
        self.username_entry.pack(pady=5)

        # Password label and entry
        password_label = tk.ttk.Label(input_frame, text="Password:")
        password_label.pack()
        self.password_entry = tk.ttk.Entry(input_frame, show="*")
        self.password_entry.pack(pady=5)

        # Create a frame for the buttons
        button_frame = tk.ttk.Frame(self)
        button_frame.pack(fill="x", pady=10)

        # Login and Register buttons
        login_button = tk.ttk.Button(button_frame, text="Login", command=self.login_user, padding=10)
        login_button.pack(side="left", padx=10)
        register_button = tk.ttk.Button(button_frame, text="Register", command=self.register_user, padding=10)
        register_button.pack(side="left", padx=10)

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, message = login(self.master.client_socket, self.master.aes_key, username, password)
        if success:
            self.master.show_file_management_page(username)
        else:
            messagebox.showinfo("Login", message)

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, message = register(self.master.client_socket, self.master.aes_key, username, password)
        messagebox.showinfo("Register", message)


class FileManagementPage(tk.ttk.Frame):
    def __init__(self, master, username):
        super().__init__(master)
        self.master = master
        self.username = username

        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the file upload section
        upload_frame = tk.ttk.Frame(self, padding=20)
        upload_frame.pack(fill="both", expand=True)

        # File upload label and button
        upload_label = tk.ttk.Label(upload_frame, text="Select a file to upload:")
        upload_label.pack()
        upload_button = tk.ttk.Button(upload_frame, text="Browse", command=self.upload_file)
        upload_button.pack(pady=5)

        # Create a frame for the file download section
        download_frame = tk.ttk.Frame(self, padding=20)
        download_frame.pack(fill="both", expand=True)

        # File download label and entry
        download_label = tk.ttk.Label(download_frame, text="Enter the file name to download:")
        download_label.pack()
        self.download_entry = tk.ttk.Entry(download_frame)
        self.download_entry.pack(pady=5)

        # Download button
        download_button = tk.ttk.Button(download_frame, text="Download", command=self.download_file)
        download_button.pack(pady=5)

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'rb') as file:
                file_data = file.read()
            file_name = file_path.split('/')[-1]
            success, message = send_file_to_server(self.master.client_socket, self.master.aes_key, self.username, file_name, file_data)
            messagebox.showinfo("Upload", message)

    def download_file(self):
        file_name = self.download_entry.get()
        success, result = request_file_from_server(self.master.client_socket, self.master.aes_key, self.username, file_name)
        if success:
            name_of_file, data_in_file = result
            file_path = filedialog.asksaveasfilename(defaultextension='.txt', initialfile=name_of_file)
            print(file_path)
            if file_path:
                with open(file_path, 'wb') as file:
                    file.write(data_in_file)
                messagebox.showinfo("Download", "File downloaded successfully.")
        else:
            messagebox.showinfo("Download", result)


if __name__ == "__main__":
    app = App()
    app.mainloop()