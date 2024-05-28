import tkinter as tk
from tkinter import messagebox, filedialog
import socket
from ttkthemes import ThemedStyle
import zlib

# Import the necessary functions from the client_functions file
from client.client_functions import generate_and_share_aes_key_with_server, login, register, send_file_to_server, \
    request_file_from_server, request_file_names


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Reed-Solomon File manager")
        self.geometry("800x800")

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
        self.style.set_theme("plastik")
        # or clearlooks,itft1,plastik,scidblue,smog

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

        self.configure_styles()
        self.create_widgets()
        self.refresh_file_list()

    def configure_styles(self):
        self.style = tk.ttk.Style()
        self.style.configure("Title.TLabel", font=("Helvetica", 16, "bold"), foreground="navy")
        self.style.configure("Instructions.TLabel", font=("Helvetica", 12, "bold"), foreground="darkgreen")
        self.style.configure("Button.TButton", font=("Helvetica", 12), background="lightblue", foreground="black", width=20, anchor="center")

    def create_widgets(self):
        # Create a frame for the title
        title_frame = tk.ttk.Frame(self, padding=20)
        title_frame.pack(fill="x")

        # Title label
        title_label = tk.ttk.Label(title_frame, text=f"File Manager\nWelcome {self.username}!", style="Title.TLabel")
        title_label.pack()

        # Create a frame for the file list section
        list_frame = tk.ttk.Frame(self, padding=20)
        list_frame.pack(fill="both", expand=True)

        # File list label and listbox
        list_label = tk.ttk.Label(list_frame, text="Available Files:", font=("Helvetica", 14))
        list_label.pack()
        self.file_listbox = tk.Listbox(list_frame, font=("Helvetica", 12), background="lightyellow", selectbackground="orange")
        self.file_listbox.pack(fill="both", expand=True)

        # Button frame
        button_frame = tk.ttk.Frame(list_frame)
        button_frame.pack()

        # Refresh button
        refresh_button = tk.ttk.Button(button_frame, text="Refresh", command=self.refresh_file_list, style="Button.TButton")
        refresh_button.pack(side="left", padx=10)

        # Download button
        download_button = tk.ttk.Button(button_frame, text="Download Selected File", command=self.download_selected_file, style="Button.TButton")
        download_button.pack(side="left", padx=10)

        # Create a frame for the file upload section
        upload_frame = tk.ttk.Frame(self, padding=20)
        upload_frame.pack(fill="x")

        # File upload label and button
        upload_label = tk.ttk.Label(upload_frame, text="Select a file to upload:", font=("Helvetica", 14))
        upload_label.pack()
        upload_button = tk.ttk.Button(upload_frame, text="Browse", command=self.upload_file, style="Button.TButton")
        upload_button.pack(pady=10)

        # Create a frame for the instructions section
        instructions_frame = tk.ttk.Frame(self, padding=10)
        instructions_frame.pack(fill="both", expand=True)

        # Instructions label and text
        instructions_label = tk.ttk.Label(instructions_frame, text="Instructions:", style="Instructions.TLabel")
        instructions_label.pack()
        instructions_text = tk.Text(instructions_frame, wrap="word", height=5, font=("Helvetica", 12), background="lightcyan")
        instructions_text.pack(fill="both", expand=True)
        instructions_text.insert(tk.END, "1. Select a file to upload using the 'Browse' button.\n")
        instructions_text.insert(tk.END, "2. Select a file from the list to download.\n")
        instructions_text.insert(tk.END, "3. Click 'Download Selected File' to download the chosen file.")
        instructions_text.configure(state="disabled")

    def refresh_file_list(self):
        success, result = request_file_names(self.master.client_socket, self.master.aes_key, self.username)
        if success:
            file_names = result
            self.file_listbox.delete(0, tk.END)
            for file_name in file_names:
                self.file_listbox.insert(tk.END, file_name)
        else:
            messagebox.showinfo("Error", result)

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'rb') as file:
                file_data = file.read()
                compressed_data = zlib.compress(file_data)

            # Check if compressed data is less than 5 KB
            if len(compressed_data) > 5 * 1024:
                messagebox.showinfo("Upload", "File size exceeds the 5 KB limit.")
                return

            file_name = file_path.split('/')[-1]
            success, message = send_file_to_server(self.master.client_socket, self.master.aes_key, self.username,
                                                   file_name, compressed_data)
            messagebox.showinfo("Upload", message)
            self.refresh_file_list()

    def download_selected_file(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            file_name = self.file_listbox.get(selected_index)
            success, result = request_file_from_server(self.master.client_socket, self.master.aes_key, self.username,
                                                       file_name)
            if success:
                name_of_file, compressed_data_in_file = result
                data_in_file = zlib.decompress(compressed_data_in_file)
                file_path = filedialog.asksaveasfilename(defaultextension='.txt', initialfile=name_of_file)
                print(file_path)
                if file_path:
                    with open(file_path, 'wb') as file:
                        file.write(data_in_file)
                    messagebox.showinfo("Download", "File downloaded successfully.")
            else:
                messagebox.showinfo("Download", result)
        else:
            messagebox.showinfo("Download", "No file selected.")


if __name__ == "__main__":
    app = App()
    app.mainloop()