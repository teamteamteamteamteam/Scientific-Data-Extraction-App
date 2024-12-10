import sqlite3
from DatabaseInterface import DatabaseInterface

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
                self.conn = sqlite3.connect(self.db_path)
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

    # Table operations
    def insert_into_table_compounds(self, compound_name, compound_concentration, smiles, is_active):
        self.cursor.execute('''
                    INSERT INTO Compounds (compound_name, compound_concentration, smiles, is_active)
                    VALUES (?, ?, ?, ?)
                ''', (compound_name, compound_concentration, smiles, is_active))
        
    def update_coords_table_compounds(self, compound_name, coord_x, coord_y):
        self.cursor.execute('''
                    UPDATE Compounds 
                    SET coord_x = ?, coord_y = ?
                    WHERE compound_name = ?
                ''', (coord_x, coord_y, compound_name))
        
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
        
    def fetch_compound_by_name_and_concentration(self, compound_name, concentration):
        self.cursor.execute('''SELECT compound_id, is_active, coord_x, coord_y 
                            FROM Compounds 
                            WHERE compound_name = ? AND compound_concentration = ?
                            ''', (compound_name, concentration))
        result = self.cursor.fetchone()
    
        if result is None:
            return None
        
        # Obsługa konwersji bajtów na float
        # coord_x = float.fromhex(result[2].hex()) if isinstance(result[2], bytes) else result[2]
        # coord_y = float.fromhex(result[3].hex()) if isinstance(result[3], bytes) else result[3]
    
        return {
            "compound_id": result[0],
            "is_active": result[1],
            "coord_x": result[2],
            "coord_y": result[3],
        }

    def find_compound_id(self, compound_name):
        self.cursor.execute("SELECT compound_id FROM Compounds WHERE compound_name = ?", (compound_name,))

    def insert_into_table_images(self, compound_id, folder_path, dapi, tubulin, actin):
        self.cursor.execute('''
                        INSERT INTO Images (compound_id, folder_path, dapi_path, tubulin_path, actin_path)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (compound_id, folder_path, dapi, actin, tubulin))
        
    def insert_into_color_by_concentration(self, r, g, b):
        self.cursor.execute('''
                        INSERT INTO Color_by_concentration (R, G, B)
                        VALUES (?, ?, ?)
                    ''', (r, g, b))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def update_compounds_color_concentration(self, concentration, color_id):
        self.cursor.execute('''
                    UPDATE Compounds 
                    SET color_id = ?
                    WHERE compound_concentration  = ?
                ''', (color_id, concentration))
        
    def insert_into_color_table_by_moa(self, moa, concentration, r, g, b):
        self.cursor.execute('''
                        INSERT INTO Color_by_moa (moa, moa_concentration, R, G, B)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (moa, concentration, r, g, b))
        self.conn.commit()
        return self.cursor.lastrowid