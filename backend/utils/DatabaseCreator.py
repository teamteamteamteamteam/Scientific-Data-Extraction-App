from DatabaseInterface import DatabaseInterface

class DatabaseCreator:
    def __init__(self, database: DatabaseInterface):
        # Connects to the database and creates tables.
        self.database = database
        self.database.connect()

    def __del__(self):
        # Closes the database connection.
        self.database.close()

    def create_table(self, table_name):
        if table_name == 'compounds':
            self.create_table_compounds()
        elif table_name == 'images':
            self.create_table_images()
        elif table_name == 'color_by_concentration':
            self.create_table_color_by_concentration()
        elif table_name == 'color_by_moa':
            self.create_table_color_by_moa()
        else:
            raise ValueError(f"Unknown table: {table_name}")

    def create_table_compounds(self):
        self.database.create_table_compounds()
        self.database.commit()

    def create_table_images(self):
        self.database.create_table_images()
        self.database.commit()

    def create_table_color_by_concentration(self):
        self.database.create_table_color_by_concentration()
        self.database.commit()

    def create_table_color_by_moa(self):
        self.database.create_table_color_by_moa()
        self.database.commit()
