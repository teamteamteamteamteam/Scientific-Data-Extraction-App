import pytest
from unittest.mock import MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.utils.DatabaseCreator import DatabaseCreator
from backend.utils.DatabaseInterface import DatabaseInterface

def test_database_creator_initialization(mocker):
    mock_database = MagicMock(spec=DatabaseInterface)
    
    creator = DatabaseCreator(mock_database)
    
    mock_database.connect.assert_called_once()

def test_create_table_compounds(mocker):
    mock_database = MagicMock(spec=DatabaseInterface)
    creator = DatabaseCreator(mock_database)
    
    creator.create_table('compounds')
    
    mock_database.create_table_compounds.assert_called_once()
    mock_database.commit.assert_called_once()

def test_create_table_images(mocker):
    mock_database = MagicMock(spec=DatabaseInterface)
    creator = DatabaseCreator(mock_database)
    
    creator.create_table('images')
    
    mock_database.create_table_images.assert_called_once()
    mock_database.commit.assert_called_once()

def test_create_table_color_by_concentration(mocker):
    mock_database = MagicMock(spec=DatabaseInterface)
    creator = DatabaseCreator(mock_database)
    
    creator.create_table('color_by_concentration')
    
    mock_database.create_table_color_by_concentration.assert_called_once()
    mock_database.commit.assert_called_once()

def test_create_table_color_by_moa(mocker):
    mock_database = MagicMock(spec=DatabaseInterface)
    creator = DatabaseCreator(mock_database)
    
    creator.create_table('color_by_moa')
    
    mock_database.create_table_color_by_moa.assert_called_once()
    mock_database.commit.assert_called_once()

def test_create_table_invalid_table(mocker):
    mock_database = MagicMock(spec=DatabaseInterface)
    creator = DatabaseCreator(mock_database)
    
    with pytest.raises(ValueError, match="Unknown table: unknown_table"):
        creator.create_table('unknown_table')