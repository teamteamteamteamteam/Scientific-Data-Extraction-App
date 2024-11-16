import csv
from DatabaseInterface import DatabaseInterface

class DatabaseFiller:

    def __init__(self, database: DatabaseInterface):
        self.database = database
        self.database.connect()
    
    def __del__(self):
        self.database.close()

    def fill_compounds_table(self, csv_file):
        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                compound_name = row['compound']
                smiles = row['smiles']
                self.database.insert_into_table_compounds(compound_name, smiles)
            
            self.database.commit()

    def fill_images_table(self, csv_file):
        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                compound_name = row['Image_Metadata_Compound']
                concentration = float(row['Image_Metadata_Concentration'])

                folder_DAPI_path = row['Image_PathName_DAPI']
                image_DAPI_path = row['Image_FileName_DAPI']

                folder_Tubulin_path = row['Image_PathName_Tubulin']
                image_Tubulin_path = row['Image_FileName_Tubulin']

                folder_Actin_path = row['Image_PathName_Actin']
                image_Actin_path = row['Image_FileName_Actin']
                
                self.database.find_compound_id(compound_name)
                compound_id_row = self.database.cursor.fetchone()

                if compound_id_row:
                    compound_id = compound_id_row[0]
                    self.database.insert_into_table_images(compound_id, concentration, folder_DAPI_path, image_DAPI_path)
                    self.database.insert_into_table_images(compound_id, concentration, folder_Tubulin_path, image_Tubulin_path)
                    self.database.insert_into_table_images(compound_id, concentration, folder_Actin_path, image_Actin_path)
                else:
                    print(f"Compound {compound_name} not found in Compounds table.")
                    raise ModuleNotFoundError
                
            self.database.commit()
    