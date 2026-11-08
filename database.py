import sqlite3

class DataBase:
    def __init__(self, name):
        self.connect = sqlite3.connect(name)
        self.cursor = self.connect.cursor()
        self.create_table()

    def create_table(self):
        connect = self.connect
        cursor = self.cursor
        command_table = "CREATE TABLE IF NOT EXISTS contacts(id INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT, age INTEGER, Phone1 TEXT, Phone2 TEXT, Phone3 TEXT, relation TEXT)"
        cursor.execute(command_table)
        connect.commit()

    def close(self):
        self.connect.close()