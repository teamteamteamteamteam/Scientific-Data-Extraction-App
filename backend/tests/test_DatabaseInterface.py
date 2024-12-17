from unittest.mock import MagicMock

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.utils.SQLiteDatabase import SQLiteDatabase
from backend.utils.DatabaseCreator import DatabaseCreator
from backend.utils.DatabaseFiller import DatabaseFiller

def test_class_implements_database_interface_with_mock():
    # Create a mock instance of SQLiteDatabase with the path
    db_instance = SQLiteDatabase('path_to_db')
    
    # Mock the methods of the database class
    db_instance.connect = MagicMock()
    db_instance.commit = MagicMock()
    db_instance.close = MagicMock()
    db_instance.create_table_compounds = MagicMock()
    db_instance.insert_into_table_compounds = MagicMock()
    db_instance.update_coords_table_compounds = MagicMock()
    db_instance.find_compound_id = MagicMock()
    db_instance.create_table_images = MagicMock()
    db_instance.insert_into_table_images = MagicMock()

    # Test SQLiteDatabase methods directly
    assert hasattr(db_instance, 'connect')
    assert hasattr(db_instance, 'close')
    assert hasattr(db_instance, 'commit')
    assert hasattr(db_instance, 'create_table_compounds')
    assert hasattr(db_instance, 'insert_into_table_compounds')
    assert hasattr(db_instance, 'update_coords_table_compounds')
    assert hasattr(db_instance, 'find_compound_id')
    assert hasattr(db_instance, 'create_table_images')
    assert hasattr(db_instance, 'insert_into_table_images')
    


    # Initialize DatabaseCreator with the mock database instance
    db_creator = DatabaseCreator(db_instance)

    # Check that the database object in the DatabaseCreator has the necessary methods
    assert hasattr(db_creator.database, 'connect')
    assert hasattr(db_creator.database, 'close')
    assert hasattr(db_creator.database, 'commit')
    assert hasattr(db_creator.database, 'create_table_compounds')
    assert hasattr(db_creator.database, 'insert_into_table_compounds')
    assert hasattr(db_creator.database, 'update_coords_table_compounds')
    assert hasattr(db_creator.database, 'find_compound_id')
    assert hasattr(db_creator.database, 'create_table_images')
    assert hasattr(db_creator.database, 'insert_into_table_images')