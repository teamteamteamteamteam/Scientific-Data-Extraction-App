import sqlite3
from .DatabaseInterface import DatabaseInterface

class SQLiteDatabase(DatabaseInterface):
    # Singleton: A single instance for the entire application
    _instance = None
    _connection_count = 0

    def __new__(cls, db_path):
        # Creates a class instance or returns the existing one (Singleton)
        if cls._instance is None:
            cls._instance = super(SQLiteDatabase, cls).__new__(cls)
            cls._instance.db_path = db_path
            cls._instance.conn = None
            cls._instance.cursor = None
        return cls._instance

    def connect(self):
        # Establishes a connection to the database if none exists
        if self.conn is None:
            try:
                self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
                self.cursor = self.conn.cursor()
                SQLiteDatabase._connection_count += 1
            except sqlite3.Error as e:
                raise RuntimeError(f"Failed to connect to the database: {e}")

    def close(self):
        # Closes the connection to the database
        SQLiteDatabase._connection_count -= 1
        if SQLiteDatabase._connection_count <= 0:
            SQLiteDatabase._connection_count = 0
            if self.cursor:
                self.cursor.close()
                self.cursor = None
            if self.conn:
                self.conn.close()
                self.conn = None

    def commit(self):
        # Commits all changes made to the database
        if self.conn:
            try:
                self.conn.commit()
            except sqlite3.Error as e:
                raise RuntimeError(f"Error during transaction commit: {e}")
        else:
            raise RuntimeError("No active database connection.")

    # Table creation methods
    def create_table_compounds(self):
        try:
            self.cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS Compounds (
                    compound_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    compound_name TEXT NOT NULL,
                    compound_concentration REAL NOT NULL,
                    smiles TEXT,
                    is_active INTEGER CHECK (is_active IN (0, 1)),
                    coord_x REAL,
                    coord_y REAL,
                    moa_id INTEGER,
                    color_id INTEGER     
                )
            ''')
        except sqlite3.Error as e:
            print(f"Error creating Compounds table: {e}")

    def create_table_images(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Images (
                    image_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    compound_id INTEGER,
                    folder_path TEXT,
                    dapi_path TEXT,
                    tubulin_path TEXT, 
                    actin_path TEXT,                    
                    FOREIGN KEY (compound_id) REFERENCES Compounds (compound_id)
                )
            ''')
        except sqlite3.Error as e:
            print(f"Error creating Images table: {e}")

    def create_table_color_by_concentration(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Color_by_concentration (
                    color_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    R REAL,
                    G REAL,
                    B REAL    
                )
            ''')
        except sqlite3.Error as e:
            print(f"Error creating Color_by_concentration table: {e}")

    def create_table_color_by_moa(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Color_by_moa (
                    moa_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    moa TEXT,
                    moa_concentration REAL,
                    R REAL,
                    G REAL,
                    B REAL
                )
            ''')
        except sqlite3.Error as e:
            print(f"Error creating Color_by_moa table: {e}")

    def create_table_tiff_images(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Tiff_images (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    compound_id INTEGER,
                    dapi_blob BLOB,
                    tubulin_blob BLOB, 
                    actin_blob BLOB
                )
            ''')
        except sqlite3.Error as e:
            print(f"Error creating tiff_images: {e}")

    # Table insert methods
    def insert_into_table_compounds(self, compound_name, compound_concentration, smiles, is_active):
        self.cursor.execute('''
                    INSERT INTO Compounds (compound_name, compound_concentration, smiles, is_active)
                    VALUES (?, ?, ?, ?)
                ''', (compound_name, compound_concentration, smiles, is_active))

    def insert_into_table_images(self, compound_id, folder_path, dapi, tubulin, actin):
        self.cursor.execute('''
                        INSERT INTO Images (compound_id, folder_path, dapi_path, tubulin_path, actin_path)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (compound_id, folder_path, dapi, actin, tubulin))
        
    def insert_into_table_tiff_images(self, compound_id, dapi_blob, tubulin_blob, actin_blob):
        self.cursor.execute('''
                        INSERT INTO Tiff_images (compound_id, dapi_blob, tubulin_blob, actin_blob)
                        VALUES (?, ?, ?, ?)
                    ''', (compound_id, dapi_blob, tubulin_blob, actin_blob))
        
    def insert_into_color_by_concentration(self, r, g, b):
        self.cursor.execute('''
                        INSERT INTO Color_by_concentration (R, G, B)
                        VALUES (?, ?, ?)
                    ''', (r, g, b))
        self.conn.commit()
        return self.cursor.lastrowid

    def insert_into_color_table_by_moa(self, moa, concentration, r, g, b):
        self.cursor.execute('''
                        INSERT INTO Color_by_moa (moa, moa_concentration, R, G, B)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (moa, concentration, r, g, b))
        self.conn.commit()
        return self.cursor.lastrowid  

    # Table update methods
    def update_compounds_moa(self, compound_name, moa_id):
        self.cursor.execute('''
                    UPDATE Compounds 
                    SET moa_id = ?
                    WHERE compound_name = ?
                ''', (moa_id, compound_name))
        
    def update_compound_coordinates(self, compound_id, new_x, new_y, is_active):
        self.cursor.execute('''
                    UPDATE Compounds 
                    SET coord_x = ?, coord_y = ?, is_active = ?
                    WHERE compound_id = ?
                ''', (round(abs(float(new_x)), 3), round(abs(float(new_y)), 3), is_active, compound_id))

    def updata_compounds_empty_moa(self, moa_id):
        self.cursor.execute('''
                    UPDATE Compounds 
                    SET moa_id = ?
                    WHERE moa_id IS NULL
                ''', (moa_id,))
        
    def update_compounds_color_concentration(self, concentration, color_id):
        self.cursor.execute('''
                    UPDATE Compounds 
                    SET color_id = ?
                    WHERE compound_concentration  = ?
                ''', (color_id, concentration))
    
    # Table fetch methods
    def fetch_compound_by_name_and_concentration(self, compound_name, concentration):
        self.cursor.execute('''SELECT compound_id, is_active, coord_x, coord_y 
                            FROM Compounds 
                            WHERE compound_name = ? AND compound_concentration = ?
                            ''', (compound_name, concentration))
        result = self.cursor.fetchone()
    
        if result is None:
            return None
    
        return {
            "compound_id": result[0],
            "is_active": result[1],
            "coord_x": result[2],
            "coord_y": result[3],
        }
    
    def fetch_all_compounds(self):
        self.cursor.execute("""
                            SELECT compound_name, compound_concentration, coord_x, coord_y
                            FROM Compounds
                            WHERE is_active = 1
                            """)
        return self.cursor.fetchall()
    
    def fetch_all_compounds_colored_by_concentration(self):
        self.cursor.execute("""
                            SELECT c.compound_name, c.compound_concentration, c.coord_x, c.coord_y, col.R, col.G, col.B
                            FROM Compounds c
                            INNER JOIN Color_by_concentration col ON c.color_id = col.color_id
                            WHERE c.is_active = 1
                            """)
        return self.cursor.fetchall()
    
    def fetch_all_compounds_colored_by_moa(self):
        self.cursor.execute("""
                            SELECT c.compound_name, c.compound_concentration, c.coord_x, c.coord_y, col.R, col.G, col.B
                            FROM Compounds c
                            INNER JOIN Color_by_moa col ON c.moa_id = col.moa_id
                            WHERE c.is_active = 1
                            """)
        return self.cursor.fetchall()

    def fetch_compound_details(self, compound_name, compound_concentration):
        self.cursor.execute("""
                            SELECT c.smiles, col.moa, col.moa_concentration
                            FROM Compounds c
                            INNER JOIN Color_by_moa col ON c.moa_id = col.moa_id
                            WHERE c.compound_name = ? AND c.compound_concentration = ?
                            """, (compound_name, compound_concentration))
        return self.cursor.fetchone()
    
    def fetch_photos_by_compound_id(self, id):
        self.cursor.execute("""
                            SELECT i.folder_path, i.dapi_path, i.tubulin_path, i.action_path
                            FROM Images i
                            WHERE i.compound_id = ? 
                            """, (id,))
        return self.cursor.fetchall()
    
    def fetch_all_images_path(self):
        self.cursor.execute("""
                            SELECT compound_id, folder_path, dapi_path, tubulin_path, actin_path 
                            FROM Images
                            """)
        
    def fetch_dapi_image(self, compound_id):
        self.cursor.execute("""
                            SELECT dapi_blob
                            FROM Tiff_images
                            WHERE compound_id = ?
                            """, (compound_id,))
        return self.cursor.fetchone()
    
    def fetch_actin_image(self, compound_id):
        self.cursor.execute("""
                            SELECT actin_blob
                            FROM Tiff_images
                            WHERE compound_id = ?
                            """, (compound_id,))
        return self.cursor.fetchone()
    
    def fetch_tubulin_image(self, compound_id):
        self.cursor.execute("""
                            SELECT tubulin_blob
                            FROM Tiff_images
                            WHERE compound_id = ?
                            """, (compound_id,))
        return self.cursor.fetchone()
    
    def fetch_all_tiff_images(self):
        self.cursor.execute("""
                            SELECT id, compound_id, length(dapi_blob), length(tubulin_blob), length(actin_blob)
                            FROM Tiff_images
                            """)
        return self.cursor.fetchall()
        

    def fetch_compound_coordinate(self, compound_name, compound_concentration):
        self.cursor.execute("""
                            SELECT c.coord_x, c.coord_y
                            FROM Compounds c
                            WHERE c.compound_name = ? AND c.compound_concentration = ?
                            """, (compound_name, compound_concentration))
        return self.cursor.fetchone()
