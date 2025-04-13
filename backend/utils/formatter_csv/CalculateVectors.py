import csv
import umap
import pandas as pd
from pathlib import Path

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.utils.UsablePaths import Paths
from backend.utils.DatabaseInterface import DatabaseInterface

class CalculateVectors:
    def __init__(self, formatted_folder_path, original_folder_path, database: DatabaseInterface):
        self.formatted_folder_path = formatted_folder_path
        self.original_folder_path = original_folder_path
        self.data = []
        self.database = database
        self.database.connect()

    def __del__(self):
        self.database.close()

    def calcualte_averange_from_file(self, folder_name):
        total_sum = 0
        total_count = 0
        chunk_size = 100

        with open(folder_name, 'r') as file:
            reader = csv.reader(file)
            next(reader)

            chunk_sum = 0
            chunk_count = 0
            buffer = []

            for i, row in enumerate(reader, start=0):
                numbers = [float(num) for num in row if num.strip()]
                buffer.append(numbers)

                if len(buffer) == chunk_size:
                    chunk_sum += sum(sum(row) for row in buffer)
                    chunk_count += sum(len(row) for row in buffer)
                    buffer.clear()

            if buffer:
                chunk_sum += sum(sum(row) for row in buffer)
                chunk_count += sum(len(row) for row in buffer)

            total_sum += chunk_sum
            total_count += chunk_count

        average = total_sum / total_count if total_count > 0 else 0
        return average

    def create_vector(self, file_paths):
        sum = 0.0
        for file_path in file_paths:
            sum += self.calcualte_averange_from_file(file_path)

        vector = sum / 3
        return vector

    def iterate_formatted_folder(self):
        path = Path(self.formatted_folder_path)
        for subfolder in path.iterdir():
            if subfolder.is_dir():
                csv_files = list(subfolder.glob("*csv"))
                vector = self.create_vector(csv_files)
                imagesList = self.find_images(subfolder.name)
                self.data.append({
                    "folder_name": subfolder.name,
                    "vector": vector,
                    "images": imagesList
                })


    def find_images(self, folder_name):
        folder_path = Path(self.original_folder_path) / folder_name

        if not folder_path.exists() or not folder_path.is_dir():
            raise FileNotFoundError(f"Folder {folder_name} does not exists in {self.original_folder_path}")

        csv_file_path = folder_path / "bbbc021_Image.csv"

        if not csv_file_path.exists() or not csv_file_path.is_file():
            raise FileNotFoundError(f"File bbbc021_Image.csv does not exists in {folder_path}")

        df = pd.read_csv(csv_file_path)

        file_names = {
            "FileName_DAPI": df["FileName_DAPI"].tolist(),
            "FileName_Tubulin": df["FileName_Tubulin"].tolist(),
            "FileName_Actin": df["FileName_Actin"].tolist(),
        }
        
        return file_names
    
    def convert_vectors_to_2D(self):
        vectors = [[entry["vector"]] for entry in self.data]
        umap_reducer = umap.UMAP(n_components=2, random_state=42)
        embeddings = umap_reducer.fit_transform(vectors)

        for entry, embedding in zip(self.data, embeddings):
            entry["x"] = embedding[0]
            entry["y"] = embedding[1]

    def save_converted_data_to_database(self):
        image_data = pd.read_csv(Paths.IMAGES_CSV_PATH)

        for entry in self.data:
            first_image_dapi = entry["images"]["FileName_DAPI"][0]
            image_row = image_data.loc[image_data["Image_FileName_DAPI"] == first_image_dapi]

            if image_row.empty:
                print(f"No data in the file for the photo {first_image_dapi}.")
                continue

            compound_name = image_row.iloc[0]["Image_Metadata_Compound"]
            concentration = image_row.iloc[0]["Image_Metadata_Concentration"]

            compound_data = self.database.fetch_compound_by_name_and_concentration(compound_name, concentration)

            compound_id = compound_data["compound_id"]
            is_active = compound_data["is_active"]
            old_x = compound_data["coord_x"]
            old_y = compound_data["coord_y"]

            if is_active == 0:
                new_x, new_y = entry["x"], entry["y"]
                self.database.update_compound_coordinates(compound_id, new_x, new_y, is_active=1)
            else:
                new_x = (old_x + entry["x"]) / 2 if old_x is not None else entry["x"]
                new_y = (old_y + entry["y"]) / 2 if old_y is not None else entry["y"]
                self.database.update_compound_coordinates(compound_id, new_x, new_y, is_active=1)

            for dapi, tubulin, actin in zip(
                entry["images"]["FileName_DAPI"],
                entry["images"]["FileName_Tubulin"],
                entry["images"]["FileName_Actin"]
            ):
                image_row = image_data.loc[image_data["Image_FileName_DAPI"] == dapi]

                if image_row.empty:
                    print(f"Brak danych w pliku dla zdjęcia {dapi}.")
                    continue

                folder_path = image_row.iloc[0]["Image_PathName_DAPI"]
                
                self.database.insert_into_table_images(compound_id, folder_path, dapi, tubulin, actin)

            self.database.commit()