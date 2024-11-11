import csv
import sqlite3

class DatabaseFiller:

    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        return conn

    def fill_data_from_images_csv(self, csv_file, table_name):
        conn = self.connect()
        cursor = conn.cursor()

        # Open the CSV file and read the data
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