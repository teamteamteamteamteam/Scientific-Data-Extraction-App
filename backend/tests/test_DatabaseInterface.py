import pytest
from unittest.mock import MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.utils.SQLiteDatabase import SQLiteDatabase
from backend.utils.DatabaseCreator import DatabaseCreator
from backend.utils.DatabaseInterface import DatabaseInterface
from backend.utils.DatabaseFiller import DatabaseFiller

@pytest.fixture
def mock_database():
    # Mock an SQLiteDatabase instance
    db_instance = MagicMock(spec=SQLiteDatabase)
    return db_instance

def test_sqlite_database_implements_all_interface_methods(mock_database):
    # Test if SQLiteDatabase implements all methods from DatabaseInterface
    interface_methods = [
        method for method in dir(DatabaseInterface)
        if callable(getattr(DatabaseInterface, method)) and not method.startswith("__")
    ]

    for method in interface_methods:
        assert hasattr(mock_database, method), f"Method {method} is not implemented in SQLiteDatabase"

def test_database_creator_uses_database_interface(mock_database):
    # Test if DatabaseCreator uses a database that implements DatabaseInterface
    db_creator = DatabaseCreator(mock_database)

    interface_methods = [
        method for method in dir(DatabaseInterface)
        if callable(getattr(DatabaseInterface, method)) and not method.startswith("__")
    ]

    for method in interface_methods:
        assert hasattr(db_creator.database, method), f"Method {method} is missing in DatabaseCreator's database"

def test_database_filler_uses_database_interface(mock_database):
    # Test if DatabaseFiller uses a database that implements DatabaseInterface
    db_filler = DatabaseFiller(mock_database)

    interface_methods = [
        method for method in dir(DatabaseInterface)
        if callable(getattr(DatabaseInterface, method)) and not method.startswith("__")
    ]

    for method in interface_methods:
        assert hasattr(db_filler.database, method), f"Method {method} is missing in DatabaseFiller's database"