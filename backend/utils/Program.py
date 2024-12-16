from DatabaseCreator import *
from DatabaseFiller import *
from UsablePaths import Paths
from SQLiteDatabase import SQLiteDatabase
from formatter_csv.CalculateVectors import CalculateVectors
from pathlib import Path

database = SQLiteDatabase(Paths.DATABASE_PATH)

# Creating tables
db_creator = DatabaseCreator(database)
db_creator.create_table('compounds')
db_creator.create_table('images')
db_creator.create_table('color_by_concentration')
db_creator.create_table('color_by_moa')

# Filling tables with initial data
db_filler_compounds = DatabaseFiller(database)
db_filler_compounds.fill_initial_data()

formatted_folder_path = Path(__file__).parent / "formatter_csv" / "formatted"
original_folder_path = Path(__file__).parent / "formatter_csv" / "original"
calculateVectors = CalculateVectors(str(formatted_folder_path), str(original_folder_path), database)
calculateVectors.iterate_formatted_folder()
calculateVectors.convert_vectors_to_2D()
calculateVectors.save_converted_data_to_database()
