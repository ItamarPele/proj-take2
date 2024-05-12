import sqlite3


class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

    def add_user(self, user_id, username, password_hash, salt):
        try:
            self.cursor.execute("INSERT INTO User (USER_ID, username, password_hash, salt) VALUES (?, ?, ?, ?)",
                                (user_id, username, password_hash, salt))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"Error: Username '{username}' already exists.")

    def add_file(self, file_id, file_name, point_0, n, max2, user_id):
        self.cursor.execute(
            "INSERT INTO File (file_ID, file_name, point_0, n, max2, user_id) VALUES (?, ?, ?, ?, ?, ?)",
            (file_id, file_name, point_0, n, max2, user_id))
        self.conn.commit()

    def get_user(self, user_id):
        self.cursor.execute("SELECT * FROM User WHERE USER_ID = ?", (user_id,))
        return self.cursor.fetchone()

    def get_file(self, file_id):
        self.cursor.execute("SELECT * FROM File WHERE file_ID = ?", (file_id,))
        return self.cursor.fetchone()

    def username_exists(self, username):
        self.cursor.execute("SELECT 1 FROM User WHERE username = ?", (username,))
        result = self.cursor.fetchone()
        return result is not None


if __name__ == "__main__":
    print("here!")
    my_db = DatabaseManager(r"C:\Users\itama\PycharmProjects\ProjREALNOWPLEASWORK\server\db\file_test.sqlite3")
    user = my_db.get_user(123)
    print(user)
