import csv
import random
import pandas as pd
from DatabaseInterface import DatabaseInterface
from UsablePaths import Paths

class DatabaseFiller:
    def __init__(self, database: DatabaseInterface):
        self.database = database
        self.set_compounds()
        self.database.connect()
    
    def __del__(self):
        self.database.close()

    def fill_initial_data(self):
        self.fill_compounds_table()
        self.fill_color_concentration_tables()
        self.fill_color_moa_tables()

    def set_compounds(self):
        image_data = pd.read_csv(Paths.IMAGES_CSV_PATH)
        self.compounds = image_data[["Image_Metadata_Compound", "Image_Metadata_Concentration"]].drop_duplicates()
        
    def fill_compounds_table(self):
        for _, compound in self.compounds.iterrows():
            self.database.insert_into_table_compounds(compound["Image_Metadata_Compound"], 
                                                  compound["Image_Metadata_Concentration"], 
                                                  0)
        self.database.commit()

    def fill_color_concentration_tables(self):
        concentrations = self.compounds["Image_Metadata_Concentration"].unique()
        colors = self.generate_unique_colors(concentrations)

        for concentration, (r, g, b) in colors.items():
           color_id = self.database.insert_into_color_by_concentration(r, g, b)
           self.database.update_compounds_color_concentration(concentration, color_id)
        self.database.commit()

    def generate_unique_colors(self, concentrations):
        colors = {}
        used_colors = set()
        
        for concentration in concentrations:
            while True:
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                
                if (r, g, b) not in used_colors:
                    used_colors.add((r, g, b))
                    colors[concentration] = (r, g, b)
                    break
        
        return colors
    
    def fill_color_moa_tables(self):
        moa_data = pd.read_csv(Paths.MOA_CSV_PATH)
        moa_with_concentraction = moa_data[["moa", "concentration"]].drop_duplicates()
        whole_data = moa_data[["compound", "concentration", "moa"]]
        
        colors = self.generate_unique_colors_except(moa_with_concentraction, except_color=(128, 128, 128))

        for _, row in whole_data.iterrows():
            compound_name = row["compound"]
            concentration = row["concentration"]
            moa = row["moa"]

            r, g, b = colors[(moa, concentration)]

            moa_id = self.database.insert_into_color_table_by_moa(moa, concentration, r, g, b)
            self.database.update_compounds_moa(compound_name, moa_id)

        moa_id = self.database.insert_into_color_table_by_moa(None, None, 128, 128, 128)
        self.database.updata_compounds_empty_moa(moa_id)
        self.database.commit()


    def generate_unique_colors_except(self, moa_with_concentraction, except_color=(128, 128, 128)):
        colors = {}
        used_colors = set()
        used_colors.add(except_color)  # forbidden color gray
        
        for _, row in moa_with_concentraction.iterrows():
            moa = row["moa"]
            concentration = row["concentration"]

            while True:
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                
                if (r, g, b) not in used_colors and (r, g, b) not in except_color:
                    used_colors.add((r, g, b))
                    colors[(moa, concentration)] = (r, g, b)
                    break

        return colors

