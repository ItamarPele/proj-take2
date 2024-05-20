import tkinter as tk
from tkinter import messagebox
import socket
from ttkthemes import ThemedStyle

# Import the necessary functions from the client_functions file
from client.client_functions import generate_and_share_aes_key_with_server, login, register


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Authentication App")
        self.geometry("500x400")

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 5555))
        self.aes_key = generate_and_share_aes_key_with_server(self.client_socket)

        self.configure_styles()

        # Create the UI elements
        self.create_widgets()

    def configure_styles(self):
        # Configure the theme
        self.style = ThemedStyle(self)
        self.style.set_theme("clearlooks")
        #or clearlooks,itft1,plastik,scidblue,smog

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
        success, message = login(self.client_socket, self.aes_key, username, password)
        messagebox.showinfo("Login", message)

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, message = register(self.client_socket, self.aes_key, username, password)
        messagebox.showinfo("Register", message)


if __name__ == "__main__":
    app = App()
    app.mainloop()
