from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def connect(self):
        pass # pragma: no cover

    @abstractmethod
    def close(self):
        pass # pragma: no cover

    @abstractmethod
    def commit(self):
        pass # pragma: no cover

    @abstractmethod
    def create_table_compounds(self):
        pass # pragma: no cover
    
    @abstractmethod
    def insert_into_table_compounds(self, compound_name, compound_concentration, smiles, is_active):
        pass # pragma: no cover

    @abstractmethod
    def update_compounds_moa(self, compound_name, moa_id):
        pass # pragma: no cover

    @abstractmethod
    def updata_compounds_empty_moa(self, moa_id):
        pass # pragma: no cover

    @abstractmethod
    def update_compound_coordinates(self, compound_id, new_x, new_y, is_active):
        pass # pragma: no cover

    @abstractmethod
    def fetch_compound_by_name_and_concentration(self, compound_name, concentration):
        pass # pragma: no cover

    @abstractmethod
    def fetch_all_compounds(self):
        pass # pragma: no cover

    @abstractmethod
    def fetch_all_compounds_colored_by_concentration(self):
        pass # pragma: no cover

    @abstractmethod
    def fetch_all_compounds_colored_by_moa(self):
        pass # pragma: no cover

    @abstractmethod
    def fetch_compound_details(self, compound_name, compound_concentration):
        pass # pragma: no cover
    
    @abstractmethod
    def create_table_images(self):
        pass # pragma: no cover

    @abstractmethod
    def insert_into_table_images(self, compound_id, folder_path, dapi, tubulin, actin):
        pass # pragma: no cover

    @abstractmethod
    def create_table_color_by_concentration(self):
        pass # pragma: no cover

    @abstractmethod
    def insert_into_color_by_concentration(self, r, g, b):
        pass # pragma: no cover

    @abstractmethod
    def create_table_color_by_moa(self):
        pass # pragma: no cover

    @abstractmethod
    def update_compounds_color_concentration(self, concentration, color_id):
        pass # pragma: no cover

    @abstractmethod
    def insert_into_color_table_by_moa(self, moa, concentration, r, g, b):
        pass # pragma: no cover

    @abstractmethod
    def fetch_photos_by_compound_id(self, id):
        pass # pragma: no cover

    @abstractmethod
    def create_table_tiff_images(self):
        pass # pragma: no cover

    @abstractmethod
    def insert_into_table_tiff_images(self, compound_id, dapi_blob, tubulin_blob, actin_blob):
        pass # pragma: no cover

    @abstractmethod
    def fetch_all_images_path(self):
        pass # pragma: no cover

    @abstractmethod
    def fetch_dapi_image(self, compound_id):
        pass # pragma: no cover

    @abstractmethod
    def fetch_actin_image(self, compound_id):
        pass # pragma: no cover

    @abstractmethod
    def fetch_tubulin_image(self, compound_id):
        pass # pragma: no cover

    @abstractmethod
    def fetch_all_tiff_images(self):
        pass # pragma: no cover