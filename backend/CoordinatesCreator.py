import pandas as pd
import numpy as np
import umap
from rdkit import Chem
from rdkit.Chem import AllChem
from DatabaseInterface import DatabaseInterface

class CoordinatesCreator:
    def __init__(self, database: DatabaseInterface):
        self.database = database
        self.database.connect()
        self.second_special_coordinate = 0.5
        self.coordinates = {} 

    def __del__(self):
        self.database.close()

    def get_special_coordinate(self):
        coord_x = self.second_special_coordinate 
        coord_y = 0.0 
        self.second_special_coordinate += 0.5
        return coord_x, coord_y
    
    def generate_fingerprint(self, smiles):
        mol = Chem.MolFromSmiles(smiles)
        if mol is not None:
            return AllChem.GetMorganFingerprintAsBitVect(mol, radius=2, nBits=1024)
        else:
            return None

    def calculate_coordinates(self, csv_file):
        data = pd.read_csv(csv_file, usecols=['compound', 'smiles'], encoding='utf-8')

        # Generate fingerprints only for SMILES compounds
        data['fingerprint'] = data['smiles'].apply(
            lambda smiles: self.generate_fingerprint(smiles) if pd.notnull(smiles) and smiles != "" else None
        )

        # Creating a fingerprint matrix for SMILES (we skip None)
        fingerprints = [fp.ToBitString() for fp in data['fingerprint'] if fp is not None]
        fingerprint_matrix = np.array([[int(bit) for bit in fp] for fp in fingerprints])

        # Reducing dimensions to 2D using UMAP
        umap_reducer = umap.UMAP(n_components=2, random_state=42)
        embedding = umap_reducer.fit_transform(fingerprint_matrix)

        embedding_index = 0
        for _, row in data.iterrows():
            compound_name = row['compound']
            
            if row['fingerprint'] is not None:
                coord_x, coord_y = embedding[embedding_index]
                embedding_index += 1
            else:
                coord_x, coord_y = self.get_special_coordinate()

            self.database.update_coords_table_compounds(compound_name, float(coord_x), float(coord_y))
        
        self.database.commit()