from DatabaseInterface import DatabaseInterface

class DatabaseCreator:

    def __init__(self, database: DatabaseInterface):
        self.database = database
        self.database.connect()

    def __del__(self):
        self.database.close()

    def create_table_compounds(self):
        self.database.create_table_compounds()
        self.database.commit()

    def create_table_images(self):
        self.database.create_table_images()
        self.database.commit()
