import random
import pandas as pd
from .DatabaseInterface import DatabaseInterface
from .UsablePaths import Paths

class DatabaseFiller:
    def __init__(self, database: DatabaseInterface):
        self.database = database
        self.set_compounds()  # Initialize compound data from the CSV file
        self.database.connect()  # Connect to the database
    
    def __del__(self):
        self.database.close()  # Ensure database connection is closed when the object is destroyed

    def set_compounds(self):
        image_data = pd.read_csv(Paths.IMAGES_CSV_PATH)  # Reading image data from a CSV file

        # Extracting unique combinations of compound and concentration
        self.compounds = image_data[["Image_Metadata_Compound", "Image_Metadata_Concentration"]].drop_duplicates()

    def fill_initial_data(self):
        self.fill_compounds_table()  # Populate compounds table
        self.fill_color_concentration_tables()  # Add color associations for concentrations
        self.fill_color_moa_tables()  # Add color associations for MOA (Mechanism of Action)

    def fill_compounds_table(self):
        smiles_data = pd.read_csv(Paths.COMPOUND_CSV_PATH)  # Load compound-to-SMILES data

        # Creating a dictionary mapping compounds to their SMILES representation
        smiles_mapping = dict(zip(smiles_data["compound"], smiles_data["smiles"])) # Map {compound: smiles}

        for _, compound in self.compounds.iterrows():
            # Getting the SMILES value for the compound or None if not found
            smiles_value = smiles_mapping.get(compound["Image_Metadata_Compound"], None)

            self.database.insert_into_table_compounds(compound["Image_Metadata_Compound"], 
                                                      compound["Image_Metadata_Concentration"], 
                                                      smiles_value,
                                                      0)
        self.database.commit()

    def generate_unique_colors(self, concentrations):
        colors = {}  # Dictionary to store generated colors for each concentration
        used_colors = set()  # Set to track used colors
        
        for concentration in concentrations:
            while True:
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                
                if (r, g, b) not in used_colors:  # Ensuring the color is unique
                    used_colors.add((r, g, b))  # Marking the color as used
                    colors[concentration] = (r, g, b)  # Associating the color with the concentration
                    break
        
        return colors  # Returning the generated colors
    
    def fill_color_concentration_tables(self):
        concentrations = self.compounds["Image_Metadata_Concentration"].unique() # Extracting unique concentrations
        colors = self.generate_unique_colors(concentrations)  # Generating unique colors for each concentration

        for concentration, (r, g, b) in colors.items():
           color_id = self.database.insert_into_color_by_concentration(r, g, b)
           self.database.update_compounds_color_concentration(concentration, color_id)
        self.database.commit()

    def generate_unique_colors_except(self, moa_with_concentration, except_color=(128, 128, 128)):
        colors = {}  # Dictionary to store generated colors for each MOA and concentration combination
        used_colors = set()  # Set to track used colors
        used_colors.add(except_color)  # Adding the forbidden gray color to the used set
        
        for _, row in moa_with_concentration.iterrows():
            moa = row["moa"]
            concentration = row["concentration"]

            while True:
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                
                # Ensuring the color is unique and not the forbidden color
                if (r, g, b) not in used_colors and (r, g, b) != except_color:
                    used_colors.add((r, g, b))  # Marking the color as used
                    colors[(moa, concentration)] = (r, g, b)  # Associating the color with MOA and concentration
                    break
        return colors

    def fill_color_moa_tables(self):
        moa_data = pd.read_csv(Paths.MOA_CSV_PATH)  # Reading MOA data from a CSV file

        # Extracting unique MOA and concentration combinations
        moa_with_concentration = moa_data[["moa", "concentration"]].drop_duplicates()
        whole_data = moa_data[["compound", "concentration", "moa"]]  # Extracting compound-related MOA data.
        colors = self.generate_unique_colors_except(moa_with_concentration, except_color=(128, 128, 128))

        for _, row in whole_data.iterrows():
            compound_name = row["compound"]
            concentration = row["concentration"]
            moa = row["moa"]

            r, g, b = colors[(moa, concentration)]  # Fetching the generated color
            moa_id = self.database.insert_into_color_table_by_moa(moa, concentration, r, g, b)
            self.database.update_compounds_moa(compound_name, moa_id)

        # Inserting a default gray color for compounds without MOA
        moa_id = self.database.insert_into_color_table_by_moa(None, None, 128, 128, 128)
        self.database.updata_compounds_empty_moa(moa_id)
        self.database.commit()