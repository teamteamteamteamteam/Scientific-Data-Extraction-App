from DatabaseCreator import *
from DatabaseFiller import *
from UsablePaths import Paths
from SQLiteDatabase import SQLiteDatabase
# from CoordinatesCreator import CoordinatesCreator



database = SQLiteDatabase(Paths.DATABASE_PATH)

# Creating tables
db_creator = DatabaseCreator(database)
db_creator.create_table('compounds')
db_creator.create_table('images')
db_creator.create_table('color_by_concentration')
db_creator.create_table('color_by_moa')

# # Wypełnianie tabeli związków chemicznych
# db_filler_compounds = CompoundsDatabaseFiller(database)
# db_filler_compounds.fill_data_from_csv(Paths.COMPOUND_CSV_PATH, 'compounds')

# # Wypełnianie tabeli obrazów
# db_filler_images = ImagesDatabaseFiller(database)
# db_filler_images.fill_data_from_csv(Paths.IMAGES_CSV_PATH, 'images')

# db_coordinates = CoordinatesCreator(database)
# db_coordinates.calculate_coordinates(Paths.COMPOUND_CSV_PATH)