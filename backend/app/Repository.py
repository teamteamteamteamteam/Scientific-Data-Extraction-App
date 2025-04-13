from ..utils.SQLiteDatabase import SQLiteDatabase
from ..utils.UsablePaths import Paths

class Repository:

    def __init__(self):
        self.database = SQLiteDatabase(Paths.DATABASE_PATH)
        self.database.connect()

    def __del__(self):
        self.database.close()

    def get_all_compounds(self):
        results = self.database.fetch_all_compounds()
        return [
            {"name": row[0], "concentration": row[1], "x": row[2], "y": row[3]}
            for row in results
        ]
    
    def get_all_compounds_colored_by_concentration(self):
        results = self.database.fetch_all_compounds_colored_by_concentration()
        return [
            {
                "name": row[0], 
                "concentration": row[1], 
                "x": row[2], "y": row[3],
                "color": {"R": row[4], "G": row[5], "B": row[6]}
            }
            for row in results
        ]

    def get_all_compounds_colored_by_moa(self):
        results = self.database.fetch_all_compounds_colored_by_moa()
        return [
            {
                "name": row[0], 
                "concentration": row[1], 
                "x": row[2], "y": row[3],
                "color": {"R": row[4], "G": row[5], "B": row[6]}
            }
            for row in results
        ]

    def get_compound_details(self, compound_name, compound_concentration):
        results = self.database.fetch_compound_details(compound_name, compound_concentration)
        return [
            {
            "smiles": results[0], 
            "moa": results[1], 
            "moa_concentration": results[2]
            }
        ]
    
    def get_image_by_type(self, compound_id: str, image_type: str):
        result = ()
        match image_type:
            case "dapi": 
                result = self.database.fetch_dapi_image(compound_id, image_type)
            case "actin":
                result = self.database.fetch_actin_image(compound_id, image_type)
            case "tubulin":
                result = self.database.fetch_tubulin_image(compound_id, image_type)
            case _:
                return None
        
        if result and isinstance(result, tuple) and len(result) > 0:
            return result[0]
        return None
    def get_compound_coordinates(self, compound_name, compound_concentration):
        results = self.database.fetch_compound_coordinate(compound_name, compound_concentration)
        return {
            "coord_x": results[0], 
            "coord_y": results[1], 
            }
        
        

