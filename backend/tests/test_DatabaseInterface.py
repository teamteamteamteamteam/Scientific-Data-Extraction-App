import pytest
from unittest.mock import MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.utils.SQLiteDatabase import SQLiteDatabase

@pytest.fixture
def mock_database():
    # Tworzymy mock obiektu SQLiteDatabase
    return MagicMock(spec=SQLiteDatabase)

def test_connect(mock_database):
    mock_database.connect()
    mock_database.connect.assert_called_once()

def test_close(mock_database):
    mock_database.close()
    mock_database.close.assert_called_once()

def test_commit(mock_database):
    mock_database.commit()
    mock_database.commit.assert_called_once()

def test_create_table_compounds(mock_database):
    mock_database.create_table_compounds()
    mock_database.create_table_compounds.assert_called_once()

def test_insert_into_table_compounds(mock_database):
    mock_database.insert_into_table_compounds("Test Compound", 100.0, "C6H12O6", True)
    mock_database.insert_into_table_compounds.assert_called_once_with("Test Compound", 100.0, "C6H12O6", True)

def test_update_compounds_moa(mock_database):
    mock_database.update_compounds_moa("Test Compound", 1)
    mock_database.update_compounds_moa.assert_called_once_with("Test Compound", 1)

def test_update_compound_coordinates(mock_database):
    mock_database.update_compound_coordinates(1, 100.0, 200.0, True)
    mock_database.update_compound_coordinates.assert_called_once_with(1, 100.0, 200.0, True)

def test_fetch_compound_by_name_and_concentration(mock_database):
    mock_database.fetch_compound_by_name_and_concentration("Test Compound", 100.0)
    mock_database.fetch_compound_by_name_and_concentration.assert_called_once_with("Test Compound", 100.0)

def test_fetch_all_compounds(mock_database):
    mock_database.fetch_all_compounds()
    mock_database.fetch_all_compounds.assert_called_once()

def test_fetch_all_compounds_colored_by_concentration(mock_database):
    mock_database.fetch_all_compounds_colored_by_concentration()
    mock_database.fetch_all_compounds_colored_by_concentration.assert_called_once()

def test_insert_into_color_by_concentration(mock_database):
    mock_database.insert_into_color_by_concentration(255, 0, 0)
    mock_database.insert_into_color_by_concentration.assert_called_once_with(255, 0, 0)

def test_insert_into_color_table_by_moa(mock_database):
    mock_database.insert_into_color_table_by_moa("MOA1", 100.0, 255, 0, 0)
    mock_database.insert_into_color_table_by_moa.assert_called_once_with("MOA1", 100.0, 255, 0, 0)