import csv
import umap
import pandas as pd
from pathlib import Path

class CalculateVectors:
    def __init__(self, formatted_folder_path, original_folder_path):
        self.formatted_folder_path = formatted_folder_path
        self.original_folder_path = original_folder_path
        self.data = []

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
            "FileName_Actin": df["FileName_Actin"].tolist(),
            "FileName_DAPI": df["FileName_DAPI"].tolist(),
            "FileName_Tubulin": df["FileName_Tubulin"].tolist(),
        }

        return file_names
    
    def convert_vectors_to_2D(self):
        vectors = [[entry["vector"]] for entry in self.data]
        umap_reducer = umap.UMAP(n_components=2, random_state=42)
        embeddings = umap_reducer.fit_transform(vectors)

        for entry, embedding in zip(self.data, embeddings):
            entry["x"] = embedding[0]
            entry["y"] = embedding[1]

    def print_converted_data(self):
        for entry in self.data:
            print(f"Folder: {entry['folder_name']}, Współrzędne: ({entry['x']}, {entry['y']})")
            # print(f"Zdjęcia: {entry['images']}")


formatted_folder_path = Path(__file__).parent / "formatted"
original_folder_path = Path(__file__).parent / "original"
# calculateVectors = CalculateVectors(str(formatted_folder_path))
calculateVectors = CalculateVectors(str(formatted_folder_path), str(original_folder_path))
calculateVectors.iterate_formatted_folder()
calculateVectors.convert_vectors_to_2D()
calculateVectors.print_converted_data()