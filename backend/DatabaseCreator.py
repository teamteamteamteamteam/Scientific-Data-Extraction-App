import sqlite3

class DatabaseCreator:
    def __init__(self):
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def createTableCompounds(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Compounds (
            compound_id INTEGER PRIMARY KEY AUTOINCREMENT,
            compound_name TEXT NOT NULL,
            concentration REAL,
            smiles TEXT,
            coord_x REAL,
            coord_y REAL
            )
        ''')
        self.conn.commit()

    def createTableImages(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Images (
                image_id INTEGER PRIMARY KEY AUTOINCREMENT,
                compound_id INTEGER,
                folder_path TEXT,
                image_path TEXT,
                FOREIGN KEY (compound_id) REFERENCES Compounds (compound_id)
            )
        ''')
        self.conn.commit()


database = DatabaseCreator()
database.createTableCompounds()
database.createTableImages()
