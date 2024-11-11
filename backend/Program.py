from DatabaseCreator import *
from DatabaseFiller import *

database = DatabaseCreator()
database.create_table_compounds()
database.create_table_images()

db_filler = DatabaseFiller(Paths.DATABASE_PATH)
db_filler.fill_compounds_table(Paths.COMPOUND_CSV_PATH, 'Compounds')
db_filler.fill_images_table(Paths.IMAGES_CSV_PATH, 'Images')
