import csv
from DatabaseInterface import DatabaseInterface



class DatabaseFiller:
    def __init__(self, database: DatabaseInterface):
        self.database = database
        self.database.connect()
    
    def __del__(self):
        self.database.close()

    def fill_data_from_csv(self, csv_file, table_type):
        # Template method defining the general process
        self.open_csv_file(csv_file) # Opens the CSV file
        self.process_rows(table_type) # Processes the rows based on the table type
        self.commit_data() # Commits the data to the database

    def open_csv_file(self, csv_file):
        # Opens the CSV file
        self.csvfile = open(csv_file, newline='', encoding='utf-8')
        self.reader = csv.DictReader(self.csvfile)

    def process_rows(self, table_type):
        # Processes each row. This method should be overridden
        raise NotImplementedError("This method should be overridden by subclasses")

    def commit_data(self):
        # Commits data to the database
        self.database.commit()
        self.csvfile.close()

class CompoundsDatabaseFiller(DatabaseFiller):
    def process_rows(self, table_type):
        # Overrides process_rows to handle rows for the 'compounds' table
        if table_type != 'compounds':
            return

        for row in self.reader:
            compound_name = row['compound']
            smiles = row['smiles']
            self.database.insert_into_table_compounds(compound_name, smiles)

class ImagesDatabaseFiller(DatabaseFiller):
    def process_rows(self, table_type):
        # Overrides process_rows to handle rows for the 'images' table
        if table_type != 'images':
            return
        
        for row in self.reader:
            # Extracts image metadata for each row
            compound_name = row['Image_Metadata_Compound']
            concentration = float(row['Image_Metadata_Concentration'])

            # Extracts the image paths for different types of images (DAPI, Tubulin, Actin)
            folder_DAPI_path = row['Image_PathName_DAPI']
            image_DAPI_path = row['Image_FileName_DAPI']
            folder_Tubulin_path = row['Image_PathName_Tubulin']
            image_Tubulin_path = row['Image_FileName_Tubulin']
            folder_Actin_path = row['Image_PathName_Actin']
            image_Actin_path = row['Image_FileName_Actin']
            
            # Finds the compound ID using the compound name
            self.database.find_compound_id(compound_name)
            compound_id_row = self.database.cursor.fetchone()

            if compound_id_row:
                # If compound ID is found, insert image data for each image type
                compound_id = compound_id_row[0]
                self.database.insert_into_table_images(compound_id, concentration, folder_DAPI_path, image_DAPI_path)
                self.database.insert_into_table_images(compound_id, concentration, folder_Tubulin_path, image_Tubulin_path)
                self.database.insert_into_table_images(compound_id, concentration, folder_Actin_path, image_Actin_path)
            else:
                # If the compound is not found in the Compounds table, raise an error
                print(f"Compound {compound_name} not found in Compounds table.")
                raise ModuleNotFoundError