import math
from .Repository import Repository

class Service:

    def __init__(self):
        self.repository = Repository()

    def get_distances_to_compound(self, compound_name, compound_concentration):
        all_compounds = self.repository.get_all_compounds()
        this_compound = self.repository.get_compound_coordinates(compound_name, compound_concentration)

        x = this_compound["coord_x"]
        y = this_compound["coord_y"]
        
        result = []

        for compound in all_compounds:
            c_x = compound["x"]
            c_y = compound["y"]
            distance = math.sqrt((c_x - x)**2 + (c_y - y)**2)

            result.append({
                "name": compound["name"], 
                "concentration": compound["concentration"], 
                "distance" : distance
            })

        result.sort(key=lambda comp: comp["distance"])
        return result
