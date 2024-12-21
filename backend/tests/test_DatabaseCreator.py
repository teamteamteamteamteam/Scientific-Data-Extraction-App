import pytest
from unittest.mock import MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.utils.DatabaseCreator import DatabaseCreator
from backend.utils.DatabaseInterface import DatabaseInterface

# Test initialization of DatabaseCreator
def test_database_creator_initialization(mocker):
    # Mock the DatabaseInterface
    mock_database = MagicMock(spec=DatabaseInterface)
    
    # Create an instance of DatabaseCreator with the mock
    creator = DatabaseCreator(mock_database)
    
    # Verify that the connect method was called on initialization
    mock_database.connect.assert_called_once()

# Test creation of the 'compounds' table
def test_create_table_compounds(mocker):
    # Mock the DatabaseInterface
    mock_database = MagicMock(spec=DatabaseInterface)
    creator = DatabaseCreator(mock_database)
    
    # Call the method to create the 'compounds' table
    creator.create_table('compounds')
    
    # Verify that the corresponding method to create the compounds table was called
    mock_database.create_table_compounds.assert_called_once()
    mock_database.commit.assert_called_once()

# Test creation of the 'images' table
def test_create_table_images(mocker):
    mock_database = MagicMock(spec=DatabaseInterface)
    creator = DatabaseCreator(mock_database)
    
    creator.create_table('images')
    
    mock_database.create_table_images.assert_called_once()
    mock_database.commit.assert_called_once()

# Test creation of the 'color_by_concentration' table
def test_create_table_color_by_concentration(mocker):
    mock_database = MagicMock(spec=DatabaseInterface)
    creator = DatabaseCreator(mock_database)
    
    creator.create_table('color_by_concentration')
    
    mock_database.create_table_color_by_concentration.assert_called_once()
    mock_database.commit.assert_called_once()

# Test creation of the 'color_by_moa' table
def test_create_table_color_by_moa(mocker):
    mock_database = MagicMock(spec=DatabaseInterface)
    creator = DatabaseCreator(mock_database)
    
    creator.create_table('color_by_moa')
    
    mock_database.create_table_color_by_moa.assert_called_once()
    mock_database.commit.assert_called_once()

# Test for ValueError when unknown table is passed
def test_create_table_invalid_table(mocker):
    mock_database = MagicMock(spec=DatabaseInterface)
    creator = DatabaseCreator(mock_database)
    
    # Expect ValueError for an unknown table
    with pytest.raises(ValueError, match="Unknown table: unknown_table"):
        creator.create_table('unknown_table')