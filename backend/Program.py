from DatabaseCreator import *
from DatabaseFiller import *
from UsablePaths import Paths
from SQLiteDatabase import SQLiteDatabase
from CoordinatesCreator import CoordinatesCreator

database = SQLiteDatabase(Paths.DATABASE_PATH)

db_creator = DatabaseCreator(database)
db_creator.create_table_compounds()
db_creator.create_table_images()

db_filler = DatabaseFiller(database)
db_filler.fill_compounds_table(Paths.COMPOUND_CSV_PATH)
db_filler.fill_images_table(Paths.IMAGES_CSV_PATH)

db_coordinates = CoordinatesCreator(database)
db_coordinates.calculate_coordinates(Paths.COMPOUND_CSV_PATH)
