from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def commit(self):
        pass 

    @abstractmethod
    def create_table_compounds(self):
        pass
    
    @abstractmethod
    def insert_into_table_compounds(self, compound_name, smiles):
        pass

    @abstractmethod
    def update_coords_table_compounds(self, compound_name, coord_x, coord_y):
        pass

    @abstractmethod
    def find_compound_id(self, compound_name):
        pass
    
    @abstractmethod
    def create_table_images(self):
        pass

    @abstractmethod
    def insert_into_table_images(self, compound_id, concentration, folder_path, image_path):
        pass   