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

    def save_images_to_db(self):
        records = self.database.fetch_all_images_path()

        for compound_id, folder_path, dapi_path, tubulin_path, actin_path in records:
            clean_folder = folder_path.split("/", 1)[-1] # "Week..." delete

            dapi_file = os.path.join(self.folder_path, clean_folder, dapi_path) if dapi_path else None
            tubulin_file = os.path.join(self.folder_path, clean_folder, tubulin_path) if tubulin_path else None
            actin_file = os.path.join(self.folder_path, clean_folder, actin_path) if actin_path else None

            dapi_blob = self._convert_to_binary(dapi_file) if dapi_file else None
            tubulin_blob = self._convert_to_binary(tubulin_file) if tubulin_file else None
            actin_blob = self._convert_to_binary(actin_file) if actin_file else None

            self.database.insert_into_table_tiff_images(compound_id, dapi_blob, tubulin_blob, actin_blob)

        self.database.commit()

    def save_example_image_to_db(self):
        compound_id = 906
        folder_path = "Week1_22123"
        dapi_path = "Week1_150607_B02_s1_w107447158-AC76-4844-8431-E6A954BD1174.tif"
        tubulin_path = "Week1_150607_B02_s1_w23FDB0AC4-EA74-4D33-A7D4-8FFC4C9ED7C8.tif"
        actin_path = "Week1_150607_B02_s1_w429636E34-C663-4E49-84B5-3EA429CAB4CE.tif"

        dapi_file = os.path.join(self.folder_path, folder_path, dapi_path)
        tubulin_file = os.path.join(self.folder_path, folder_path, tubulin_path)
        actin_file = os.path.join(self.folder_path, folder_path, actin_path)

        dapi_blob = self._convert_to_binary(dapi_file)
        tubulin_blob = self._convert_to_binary(tubulin_file)
        actin_blob = self._convert_to_binary(actin_file)
        print("DAPI size:", len(dapi_blob) if dapi_blob else "None")
        print("Tubulin size:", len(tubulin_blob) if tubulin_blob else "None")
        print("Actin size:", len(actin_blob) if actin_blob else "None")


        self.database.insert_into_table_tiff_images(compound_id, dapi_blob, tubulin_blob, actin_blob)

        self.database.commit()

    def fetch_example(self):
        compound_id =  906
        blob = self.database.fetch_dapi_image(compound_id)
        print(blob)
        print()
        images = self.database.fetch_all_tiff_images()
        print(images)

database = SQLiteDatabase(Paths.DATABASE_PATH)

image_saver = ImageSaver(database, r"D:\studia\semestr5\projekt_zespolowy\dane")
image_saver.fetch_example()
# image_saver.create_table_tiff_images()
# image_saver.save_example_image_to_db()