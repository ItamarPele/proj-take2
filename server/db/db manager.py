import sqlite3
import hashlib
import os
import uuid


class DatabaseManager:
    def __init__(self, database_file):
        self.database_file = database_file

    def __enter__(self):
        self.conn = sqlite3.connect(self.database_file)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def _insert_user(self, user_id, username, password_hash, salt):
        self.cursor.execute("""
            INSERT INTO User (USER_ID, username, password_hash, salt)
            VALUES (?, ?, ?, ?)
        """, (user_id, username, password_hash, salt))
        self.conn.commit()

    def _insert_file(self, file_id, file_name, point_0, n, max2, user_id):
        self.cursor.execute("""
            INSERT INTO File (FILE_ID, file_name, point_0, n, max2, user_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (file_id, file_name, point_0, n, max2, user_id))
        self.conn.commit()

    def get_file(self, file_id):
        self.cursor.execute("SELECT file_name, point_0, n, max2 FROM File WHERE FILE_ID = ?", (file_id,))
        result = self.cursor.fetchone()
        if result:
            return (True, *result)
        else:
            return False, None, None, None, None

    def does_username_exist(self, username):
        self.cursor.execute("SELECT 1 FROM User WHERE username = ?", (username,))
        result = self.cursor.fetchone()
        return bool(result)

    @staticmethod
    def _hash_password(password):
        # Generate a random salt
        salt = os.urandom(16)

        # Hash the password with the salt
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        # Return the hashed password and salt
        return password_hash.hex(), salt

    def authenticate_user(self, username, password):
        # Fetch the user record from the database
        self.cursor.execute("SELECT password_hash, salt FROM User WHERE username = ?", (username,))
        result = self.cursor.fetchone()

        # If the username doesn't exist, return False
        if not result:
            return False

        # Unpack the stored password hash and salt
        password_hash, salt = result

        # Hash the provided password with the stored salt
        password_digest = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)

        # Compare the hashed password with the stored password hash
        if password_digest.hex() == password_hash:
            return True
        else:
            return False

    def add_user(self, username, password):
        # Generate a unique user ID
        user_id = str(uuid.uuid4())

        # Hash the password with a salt
        hashed_password, salt = self._hash_password(password)

        # Insert the user record into the database
        try:
            self._insert_user(user_id, username, hashed_password, salt.hex())
        except Exception as e:
            print("ERORR = USERNAME EXISTS")
            print(e)
        return user_id

    def add_file(self, file_name, point_0, n, max2, user_id):
        # Generate a unique file ID
        file_id = str(uuid.uuid4())

        # Insert the file record into the database
        self._insert_file(file_id, file_name, point_0, n, max2, user_id)

    def get_user_files(self, user_id):
        self.cursor.execute("SELECT FILE_ID, file_name FROM File WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()


if __name__ == "__main__":
    with DatabaseManager(r"C:\Users\itama\PycharmProjects\ProjREALNOWPLEASWORK\server\db\my_db.sqlite3") as db_manager:
        # ID = db_manager.add_user("ADMIN", "123")
        # db_manager.add_file("admin_file_1", "(0,1)", "3","10",ID)
        print(db_manager.get_user_files("7b9e906a-05ce-4f96-ad80-2dc80d6f55ce"))
