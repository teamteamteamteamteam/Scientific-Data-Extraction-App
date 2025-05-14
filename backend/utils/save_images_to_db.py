from .DatabaseInterface import DatabaseInterface
from .UsablePaths import Paths
from .SQLiteDatabase import SQLiteDatabase

import os

class ImageSaver:
    def __init__(self, database: DatabaseInterface, path: str):
        self.database = database
        self.database.connect()
        self.folder_path = path

    def __del__(self):
        self.database.close()  

    def create_table_tiff_images(self):
        self.database.create_table_tiff_images()
        self.database.commit()

    def _convert_to_binary(self, file_path):
        try:
            with open(file_path, "rb") as file:
                return file.read()
        except FileNotFoundError:
            print(f"File was not found: {file_path}")
            return None

    def _get_unique_images_by_compound(self, records):
        unique_rows = []
        previous_id = None

        for row in records:
            compound_id = row[0]
            if compound_id != previous_id:
                unique_rows.append(row)
                previous_id = compound_id
        
        return unique_rows
    
    def save_images_to_db(self):
        records = self.database.fetch_all_images_path()
        unique_rows = self._get_unique_images_by_compound(records)

        for compound_id, folder_path, dapi_path, tubulin_path, actin_path in unique_rows:
            clean_folder = folder_path.split("/", 1)[-1] # "Week..." delete

            dapi_file = os.path.join(self.folder_path, clean_folder, dapi_path) if dapi_path else None
            tubulin_file = os.path.join(self.folder_path, clean_folder, tubulin_path) if tubulin_path else None
            actin_file = os.path.join(self.folder_path, clean_folder, actin_path) if actin_path else None

            dapi_blob = self._convert_to_binary(dapi_file) if dapi_file else None
            tubulin_blob = self._convert_to_binary(tubulin_file) if tubulin_file else None
            actin_blob = self._convert_to_binary(actin_file) if actin_file else None

            self.database.insert_into_table_tiff_images(compound_id, dapi_blob, tubulin_blob, actin_blob)

        self.database.commit()

database = SQLiteDatabase(Paths.DATABASE_PATH)

image_saver = ImageSaver(database, r"[path]")
image_saver.create_table_tiff_images()
image_saver.save_images_to_db()
