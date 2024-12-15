from ..utils.SQLiteDatabase import SQLiteDatabase
from ..utils.UsablePaths import Paths

class Repository:

    def __init__(self):
        self.database = SQLiteDatabase(Paths.DATABASE_PATH)
        self.database.connect()

    def __del__(self):
        self.database.close()

    def get_all_compounds(self):
        results = self.database.fetch_all_compounds()
        return [
            {"name": row[0], "concentration": row[1], "x": row[2], "y": row[3]}
            for row in results
        ]
