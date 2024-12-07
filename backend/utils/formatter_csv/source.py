import os
from pathlib import Path
import pandas as pd

COLS_TO_SKIP = 16

class CsvFormatter:

    def __init__(self, input_folder_path, output_folder_path):
        self.input_folder_path = input_folder_path
        self.output_folder_path = output_folder_path

    def __delete_some_colls_in_csv(self, file, output_file, columns_to_skip):
        chunk_size = 1000
        with pd.read_csv(file, chunksize=chunk_size) as reader:
            with open(output_file, mode='w', encoding='utf-8', newline='') as output:

                for i, chunk in enumerate(reader):
                    chunk.drop(chunk.columns[columns_to_skip], axis=1, inplace=True)
                    chunk.fillna(0, inplace=True)
                    chunk.to_csv(output, mode='a', header=(i == 0), index=False)


    def modify_file_path(self, file_path):
        new_path = file_path.replace(self.input_folder_path, self.output_folder_path)
        base, ext = os.path.splitext(new_path)
        new_path = f"{base}_formatted{ext}"
        return new_path
    

    def create_folder(self, new_folder_name):
        new_folder_path = Path(self.output_folder_path) / new_folder_name
        new_folder_path.mkdir(exist_ok=True)
        return new_folder_path

    
    def get_csv_files(self):
        csv_files = []
        first_loop_create_dirs = True
        for root, dirs, files in os.walk(self.input_folder_path):
            
            if first_loop_create_dirs:
                first_loop_create_dirs = False
                for directory in dirs:
                    self.create_folder(directory)

            for file in files:
                if file.endswith('.csv'):
                    csv_files.append(os.path.join(root, file))
        return csv_files



    def run_formatter(self):
        os.makedirs(self.output_folder_path, exist_ok=True)
        files_to_analize = self.get_csv_files()
        cols_to_delete = [x for x in range(COLS_TO_SKIP)]
        for file_path in files_to_analize:
            if 'Image' not in file_path:
                self.__delete_some_colls_in_csv(file_path, self.modify_file_path(file_path), cols_to_delete)
                


"""
    :param input_folder_path: Nazwa folderu z danymi wejściowymi. Skrypt .py musi się znajdować
    w tym samym folderze co folder z plikami do analizy. Folder ten zawiera foldery o nazwie trzyznakowej,
    którego pliki będą analizowane.

    :param output_folder_path: Nazwa folderu, który zostanie utworzony, jeśli jeszcze nie istnieje. 
    Do tego folderu zostaną zapisane pliki wyjściowe, które wynikną z przeprowadzonej analizy.

    Przykładowe wywołanie niżej:
"""
formatted_folder_path = Path(__file__).parent / "formatted"
original_folder_path = Path(__file__).parent / "original"
# str(formatted_folder_path), str(original_folder_path)
formatter = CsvFormatter(str(original_folder_path), str(formatted_folder_path))
formatter.run_formatter()
