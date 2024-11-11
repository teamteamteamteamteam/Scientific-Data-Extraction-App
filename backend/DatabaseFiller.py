import csv
import sqlite3

class DatabaseFiller:

    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        return conn

    def fill_compounds_table(self, csv_file, table_name):
        conn = self.connect()
        cursor = conn.cursor()

        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                compound_name = row['compound']
                smiles = row['smiles']
                
                coord_x = 0.0 
                coord_y = 0.0 
                
                sql = '''INSERT INTO Compounds (compound_name, smiles, coord_x, coord_y)
                         VALUES (?, ?, ?, ?)'''
                cursor.execute(sql, (compound_name, smiles, coord_x, coord_y))
    

        conn.commit()
        conn.close()

    def fill_images_table(self, csv_file, table_name):
        conn = self.connect()
        cursor = conn.cursor()

        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                compound_name = row['Image_Metadata_Compound']
                concentration = float(row['Image_Metadata_Concentration'])
                folder_path = row['Image_PathName_DAPI']
                image_path = row['Image_FileName_DAPI']
                
                #find compound id in compounds table
                cursor.execute("SELECT compound_id FROM Compounds WHERE compound_name = ?", (compound_name,))
                compound_id_row = cursor.fetchone()

                if compound_id_row:
                    compound_id = compound_id_row[0]
                    
                    cursor.execute('''
                        INSERT INTO Images (compound_id, concentration, folder_path, image_path)
                        VALUES (?, ?, ?, ?)
                    ''', (compound_id, concentration, folder_path, image_path))

                else:
                    print(f"Compound {compound_name} not found in Compounds table.")
                    raise ModuleNotFoundError
                
            
        conn.commit()
        conn.close()
    