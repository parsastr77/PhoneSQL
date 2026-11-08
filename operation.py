from database import DataBase

class CRUD:
    def __init__(self):
        self.db = DataBase("contacts.db")

    # C
    def create(self, fname, lname, age, phone1, phone2, phone3, relat):
        self.db.cursor.execute("""INSERT INTO contacts (firstname, lastname, age, phone1, phone2, phone3, relation) VALUES 
        (?, ?, ?, ?, ?, ?, ?)""", (fname, lname, age, phone1, phone2, phone3, relat))
        self.db.connect.commit()
        

    # R
    def read(self):
        self.db.cursor.execute("SELECT * FROM contacts")
        return self.db.cursor.fetchall()

    # U
    def update(self, id, fname, lname, age, phone1, phone2, phone3, relative):
        self.db.cursor.execute("""
        UPDATE contacts
        SET firstname=?, lastname=?, age=?, phone1=?, phone2=?, phone3=?, relation=?
        WHERE id=?
        """, (fname, lname, age, phone1, phone2, phone3, relative, id))
        self.db.connect.commit()

    # D
    def delete(self, id):
        self.db.cursor.execute("DELETE FROM contacts WHERE id=?", (id,))
        self.db.connect.commit()