from pathlib import Path



#Path has got overloaded / operator for differenet os
class Paths:
    database_folder = Path.cwd() / 'backend' / 'database'
    resources_folder = Path.cwd() / 'backend' / 'resources'

    DATABASE_PATH = database_folder / 'database.db'
    COMPOUND_CSV_PATH = resources_folder / 'BBBC021_v1_compound.csv'
    IMAGES_CSV_PATH = resources_folder / 'BBBC021_v1_image.csv'
    MOA_CSV_PATH = resources_folder / 'BBBC021_v1_moa.csv'