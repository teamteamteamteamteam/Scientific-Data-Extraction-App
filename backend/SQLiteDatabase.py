import sqlite3
from DatabaseInterface import DatabaseInterface

class SQLiteDatabase(DatabaseInterface):
    _instance = None
    _connection_count = 0

    def __new__(cls, db_path):
        if cls._instance is None:
            cls._instance = super(SQLiteDatabase, cls).__new__(cls)
            cls._instance.db_path = db_path
            cls._instance.conn = None
            cls._instance.cursor = None
        return cls._instance

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        SQLiteDatabase._connection_count += 1

    def close(self):
        SQLiteDatabase._connection_count -= 1
        if SQLiteDatabase._connection_count == 0:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            self.cursor = None
            self.conn = None


    def commit(self):
        self.conn.commit()

    def create_table_compounds(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Compounds (
                compound_id INTEGER PRIMARY KEY AUTOINCREMENT,
                compound_name TEXT NOT NULL,
                smiles TEXT,
                coord_x REAL,
                coord_y REAL
            )
        ''')

    def create_table_images(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Images (
                image_id INTEGER PRIMARY KEY AUTOINCREMENT,
                compound_id INTEGER,
                concentration REAL,
                folder_path TEXT,
                image_path TEXT,
                FOREIGN KEY (compound_id) REFERENCES Compounds (compound_id)
            )
        ''')

    def insert_into_table_compounds(self, compound_name, smiles):
        self.cursor.execute('''
                    INSERT INTO Compounds (compound_name, smiles)
                    VALUES (?, ?)
                ''', (compound_name, smiles))
        
    def update_coords_table_compounds(self, compound_name, coord_x, coord_y):
        self.cursor.execute('''
                    UPDATE Compounds 
                    SET coord_x = ?, coord_y = ?
                    WHERE compound_name = ?
                ''', (coord_x, coord_y, compound_name))


    def find_compound_id(self, compound_name):
        self.cursor.execute("SELECT compound_id FROM Compounds WHERE compound_name = ?", (compound_name,))

    def insert_into_table_images(self, compound_id, concentration, folder_path, image_path):
        self.cursor.execute('''
                        INSERT INTO Images (compound_id, concentration, folder_path, image_path)
                        VALUES (?, ?, ?, ?)
                    ''', (compound_id, concentration, folder_path, image_path))