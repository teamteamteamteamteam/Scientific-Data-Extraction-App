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
    def insert_into_table_compounds(self, compound_name, compound_concentration, smiles, is_active):
        pass

    @abstractmethod
    def update_coords_table_compounds(self, compound_name, coord_x, coord_y):
        pass

    @abstractmethod
    def update_compounds_moa(self, compound_name, moa_id):
        pass

    @abstractmethod
    def updata_compounds_empty_moa(self, moa_id):
        pass

    @abstractmethod
    def update_compound_coordinates(self, compound_id, new_x, new_y, is_active):
        pass

    @abstractmethod
    def fetch_compound_by_name_and_concentration(self, compound_name, concentration):
        pass

    @abstractmethod
    def find_compound_id(self, compound_name):
        pass
    
    @abstractmethod
    def create_table_images(self):
        pass

    @abstractmethod
    def insert_into_table_images(self, compound_id, folder_path, dapi, tubulin, actin):
        pass   

    @abstractmethod
    def create_table_color_by_concentration(self):
        pass

    @abstractmethod
    def insert_into_color_by_concentration(self, r, g, b):
        pass

    @abstractmethod
    def create_table_color_by_moa(self):
        pass

    @abstractmethod
    def update_compounds_color_concentration(self, concentration, color_id):
        pass

    @abstractmethod
    def insert_into_color_table_by_moa(self, moa, concentration, r, g, b):
        pass