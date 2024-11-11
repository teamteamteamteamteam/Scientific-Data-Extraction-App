from pathlib import Path
from UsablePaths import Paths
import sqlite3
from DatabaseFiller import DatabaseFiller

class DatabaseCreator:

    def __init__(self):
        self.conn = sqlite3.connect(Paths.DATABASE_PATH)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

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
        self.conn.commit()

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
        self.conn.commit()