import pytest
from unittest.mock import MagicMock
from unittest import mock
import sqlite3
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.utils.SQLiteDatabase import SQLiteDatabase

# Helper function for mocking the connection and cursor
def mock_database_connection(mocker, db):
    # Creating mocks for cursor and connection
    mock_cursor = mock.MagicMock()
    mock_connection = mock.MagicMock()

    # Assigning mocks to database instance
    db.conn = mock_connection
    db.cursor = mock_cursor
    
    # Mocking commit method and lastrowid
    mock_connection.commit = mock.MagicMock()
    mock_cursor.lastrowid = 1  # Setting a specific value for the last inserted row ID

    # Mocking connect method to avoid actual database connection
    mocker.patch.object(db, 'connect', return_value=None)
    
    # Simulating the connection
    db.connect()

    return mock_cursor, mock_connection

# Helper function for verifying SQL queries
def verify_sql_query(mock_cursor, expected_query):
    cleaned_expected_query = ''.join(expected_query.split())
    cleaned_actual_query = ''.join(mock_cursor.execute.call_args[0][0].split())
    assert cleaned_expected_query == cleaned_actual_query, f"Expected: {cleaned_expected_query}, but got: {cleaned_actual_query}"

# Singleton test
def test_singleton():
    db1 = SQLiteDatabase("test.db")
    db2 = SQLiteDatabase("test.db")
    assert db1 is db2

# Tests for connect()
def test_connect_function(mocker):
    db = SQLiteDatabase("test.db")
    mock_connect = mocker.patch('sqlite3.connect')
    db.connect()
    mock_connect.assert_called_once_with("test.db")
    assert db.conn is not None

def test_connect_raises_runtime_error(mocker):
    db = SQLiteDatabase("test.db")
    db.conn = None  # Explicitly set the initial state of `conn` to None

    # Mock sqlite3.connect to raise an sqlite3.Error
    mocker.patch('sqlite3.connect', side_effect=sqlite3.Error("Mocked connection error"))

    # Check if connect() raises the correct RuntimeError
    with pytest.raises(RuntimeError, match="Failed to connect to the database: Mocked connection error"):
        db.connect()

    # Ensure `db.conn` is still `None` after the exception
    assert db.conn is None

# Test for close()
def test_close_connection(mocker):
    # Mock connection and cursor
    mock_cursor = MagicMock()
    mock_conn = MagicMock()

    db = SQLiteDatabase("test.db")
    
    # Set conn and cursor before calling connect()
    db.conn = mock_conn
    db.cursor = mock_cursor

    # Run the test
    db.connect()  # Connect should not set conn since it is already mocked

    # Check if the cursor and connection were closed
    db.close()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

# Tests for commit
def test_commit_success(mocker):
    # Mock connection
    mock_conn = MagicMock()
    db = SQLiteDatabase("test.db")
    db.conn = mock_conn  # Set the active connection

    # Call commit
    db.commit()

    # Check if `commit` was called
    mock_conn.commit.assert_called_once()

def test_commit_raises_runtime_error_on_commit_failure(mocker):
    # Mock connection to raise an exception during `commit`
    mock_conn = MagicMock()
    mock_conn.commit.side_effect = sqlite3.Error("Mocked commit error")
    db = SQLiteDatabase("test.db")
    db.conn = mock_conn  # Set the active connection

    # Check if method raises `RuntimeError` with the correct message
    with pytest.raises(RuntimeError, match="Error during transaction commit: Mocked commit error"):
        db.commit()

def test_commit_raises_runtime_error_no_connection():
    db = SQLiteDatabase("test.db")
    db.conn = None  # No active connection

    # Check if method raises `RuntimeError` with the correct message
    with pytest.raises(RuntimeError, match="No active database connection."):
        db.commit()

# Test for table creation methods
def test_create_compounds_table(mocker):
    db = SQLiteDatabase("test.db")
    mock_cursor, _ = mock_database_connection(mocker, db)

    expected_query = '''
        CREATE TABLE IF NOT EXISTS Compounds (
            compound_id INTEGER PRIMARY KEY AUTOINCREMENT,
            compound_name TEXT NOT NULL,
            compound_concentration REAL NOT NULL,
            smiles TEXT,
            is_active INTEGER CHECK (is_active IN (0, 1)),
            coord_x REAL,
            coord_y REAL,
            moa_id INTEGER,
            color_id INTEGER
        )
    '''
    db.create_table_compounds()
    verify_sql_query(mock_cursor, expected_query)

def test_create_compounds_table_raises_error(mocker, capsys):
    db = SQLiteDatabase("test.db")
    mock_cursor = mocker.MagicMock()
    mock_cursor.execute.side_effect = sqlite3.Error("Mocked error creating Compounds table")
    db.cursor = mock_cursor

    # Run the method
    db.create_table_compounds()

    # Capture the output
    captured = capsys.readouterr()

    # Check if the error message appeared in the standard output
    assert "Error creating Compounds table: Mocked error creating Compounds table" in captured.out

def test_create_images_table(mocker):
    db = SQLiteDatabase("test.db")
    mock_cursor, _ = mock_database_connection(mocker, db)

    expected_query = '''
        CREATE TABLE IF NOT EXISTS Images (
            image_id INTEGER PRIMARY KEY AUTOINCREMENT,
            compound_id INTEGER,
            folder_path TEXT,
            dapi_path TEXT,
            tubulin_path TEXT, 
            actin_path TEXT,
            FOREIGN KEY (compound_id) REFERENCES Compounds (compound_id)
        )
    '''
    db.create_table_images()
    verify_sql_query(mock_cursor, expected_query)

def test_create_images_table_raises_error(mocker, capsys):
    db = SQLiteDatabase("test.db")
    mock_cursor = mocker.MagicMock()
    mock_cursor.execute.side_effect = sqlite3.Error("Mocked error creating Images table")
    db.cursor = mock_cursor

    # Run the method
    db.create_table_images()

    # Capture the output
    captured = capsys.readouterr()

    # Check if the error message appeared in the standard output
    assert "Error creating Images table: Mocked error creating Images table" in captured.out

def test_create_color_by_concentration_table(mocker):
    db = SQLiteDatabase("test.db")
    mock_cursor, _ = mock_database_connection(mocker, db)

    expected_query = '''
        CREATE TABLE IF NOT EXISTS Color_by_concentration (
            color_id INTEGER PRIMARY KEY AUTOINCREMENT,
            R REAL,
            G REAL,
            B REAL    
        )
    '''
    db.create_table_color_by_concentration()
    verify_sql_query(mock_cursor, expected_query)

def test_create_color_by_concentration_table_raises_error(mocker, capsys):
    db = SQLiteDatabase("test.db")
    mock_cursor = mocker.MagicMock()
    mock_cursor.execute.side_effect = sqlite3.Error("Mocked error creating Color_by_concentration table")
    db.cursor = mock_cursor

    # Run the method
    db.create_table_color_by_concentration()

    # Capture the output
    captured = capsys.readouterr()

    # Check if the error message appeared in the standard output
    assert "Error creating Color_by_concentration table: Mocked error creating Color_by_concentration table" in captured.out

def test_create_color_by_moa_table(mocker):
    db = SQLiteDatabase("test.db")
    mock_cursor, _ = mock_database_connection(mocker, db)

    expected_query = '''
        CREATE TABLE IF NOT EXISTS Color_by_moa (
            moa_id INTEGER PRIMARY KEY AUTOINCREMENT,
            moa TEXT,
            moa_concentration REAL,
            R REAL,
            G REAL,
            B REAL
        )
    '''
    db.create_table_color_by_moa()
    verify_sql_query(mock_cursor, expected_query)

def test_create_color_by_moa_table_raises_error(mocker, capsys):
    db = SQLiteDatabase("test.db")
    mock_cursor = mocker.MagicMock()
    mock_cursor.execute.side_effect = sqlite3.Error("Mocked error creating Color_by_moa table")
    db.cursor = mock_cursor

    # Run the method
    db.create_table_color_by_moa()

    # Capture the output
    captured = capsys.readouterr()

    # Check if the error message appeared in the standard output
    assert "Error creating Color_by_moa table: Mocked error creating Color_by_moa table" in captured.out

# Test for table insert methods
def test_insert_into_table_compounds(mocker):
    db = SQLiteDatabase("test.db")
    mock_cursor, _ = mock_database_connection(mocker, db)

    # Expected SQL query to be executed by the insert method
    expected_query = '''
        INSERT INTO Compounds (compound_name, compound_concentration, smiles, is_active)
        VALUES (?, ?, ?, ?)
    '''
    # Calling the insert method with sample data
    db.insert_into_table_compounds("Test Compound", 10.0, "C1=CC=CC=C1", 1)
    
    # Verifying if the SQL query was executed with the correct parameters
    verify_sql_query(mock_cursor, expected_query)

def test_insert_into_table_images(mocker):
    db = SQLiteDatabase("test.db")
    mock_cursor, _ = mock_database_connection(mocker, db)

    # Expected SQL query to be executed by the insert method
    expected_query = '''
        INSERT INTO Images (compound_id, folder_path, dapi_path, tubulin_path, actin_path)
        VALUES (?, ?, ?, ?, ?)
    '''
    # Calling the insert method with sample data
    db.insert_into_table_images(1, "/path/to/folder", "/path/to/dapi", "/path/to/tubulin", "/path/to/actin")
    
    # Verifying if the SQL query was executed with the correct parameters
    verify_sql_query(mock_cursor, expected_query)

def test_insert_into_color_by_concentration(mocker):
    db = SQLiteDatabase("test.db")

    # Mocking the connection and cursor
    mock_cursor, mock_connection = mock_database_connection(mocker, db)

    # Expected SQL query with consistent formatting
    expected_query = """
        INSERT INTO Color_by_concentration (R, G, B) 
        VALUES (?, ?, ?)
    """

    # Calling insert method with sample color data
    db.insert_into_color_by_concentration(255, 0, 0)

    # Verifying that the execute method was called with the expected query and parameters
    verify_sql_query(mock_cursor, expected_query)

    # Verifying if commit was called
    mock_connection.commit.assert_called_once()

    # Checking if the method returned the lastrowid
    assert db.insert_into_color_by_concentration(255, 0, 0) == 1

def test_insert_into_color_table_by_moa(mocker):
    db = SQLiteDatabase("test.db")

    # Mocking the connection and cursor
    mock_cursor, mock_connection = mock_database_connection(mocker, db)

    # Expected SQL query with consistent formatting
    expected_query = """
        INSERT INTO Color_by_moa (moa, moa_concentration, R, G, B) 
        VALUES (?, ?, ?, ?, ?)
    """
    
    # Calling insert method with sample data for moa and color
    db.insert_into_color_table_by_moa("Test MOA", 100.0, 0, 255, 0)

    # Verifying that the execute method was called with the expected query and parameters
    verify_sql_query(mock_cursor, expected_query)

    # Verifying if commit was called
    mock_connection.commit.assert_called_once()

    # Checking if the method returned the lastrowid
    assert db.insert_into_color_table_by_moa("Test MOA", 100.0, 0, 255, 0) == 1

# Test for table update methods
def test_update_compounds_moa(mocker):
    db = SQLiteDatabase("test.db")
    mock_cursor, _ = mock_database_connection(mocker, db)

    # Expected SQL query for updating 'moa_id' by 'compound_name'
    expected_query = '''
        UPDATE Compounds 
        SET moa_id = ?
        WHERE compound_name = ?
    '''
    # Call method with sample data
    db.update_compounds_moa("Test Compound", 123)
    # Verify that the SQL query was executed with the correct parameters
    verify_sql_query(mock_cursor, expected_query)

def test_update_compound_coordinates(mocker):
    db = SQLiteDatabase("test.db")
    mock_cursor, _ = mock_database_connection(mocker, db)

    # Expected SQL query for updating 'coord_x', 'coord_y', and 'is_active' by 'compound_id'
    expected_query = '''
        UPDATE Compounds 
        SET coord_x = ?, coord_y = ?, is_active = ?
        WHERE compound_id = ?
    '''
    # Call method with sample data for compound coordinates
    db.update_compound_coordinates(1, "100.123", "200.456", 1)
    # Verify that the SQL query was executed with the correct parameters
    verify_sql_query(mock_cursor, expected_query)

def test_updata_compounds_empty_moa(mocker):
    db = SQLiteDatabase("test.db")
    mock_cursor, _ = mock_database_connection(mocker, db)

    # Expected SQL query for updating 'moa_id' where 'moa_id' is NULL
    expected_query = '''
        UPDATE Compounds 
        SET moa_id = ?
        WHERE moa_id IS NULL
    '''
    # Call method to update compounds with missing 'moa_id'
    db.updata_compounds_empty_moa(123)
    # Verify that the SQL query was executed with the correct parameters
    verify_sql_query(mock_cursor, expected_query)

def test_update_compounds_color_concentration(mocker):
    db = SQLiteDatabase("test.db")
    mock_cursor, _ = mock_database_connection(mocker, db)

    # Expected SQL query for updating 'color_id' based on 'compound_concentration'
    expected_query = '''
        UPDATE Compounds 
        SET color_id = ?
        WHERE compound_concentration  = ?
    '''
    # Call method with sample data for concentration and color_id
    db.update_compounds_color_concentration(100.0, 1)
    # Verify that the SQL query was executed with the correct parameters
    verify_sql_query(mock_cursor, expected_query)

# Test for table fetch methods
def test_fetch_compound_by_name_and_concentration(mocker):
    db = SQLiteDatabase("test.db")
    mock_cursor, _ = mock_database_connection(mocker, db)

    # Expected SQL query for fetching compound details by name and concentration
    expected_query = '''
        SELECT compound_id, is_active, coord_x, coord_y 
        FROM Compounds 
        WHERE compound_name = ? AND compound_concentration = ?
    '''
    # Mock result for fetchone()
    mock_cursor.fetchone.return_value = (1, 1, 100.123, 200.456)
    
    # Call method with sample data
    result = db.fetch_compound_by_name_and_concentration("Test Compound", 100.0)
    
    # Verify that the SQL query was executed with the correct parameters
    verify_sql_query(mock_cursor, expected_query)
    
    # Verify that the result matches the expected dictionary format
    assert result == {
        "compound_id": 1,
        "is_active": 1,
        "coord_x": 100.123,
        "coord_y": 200.456
    }

    # Test when no result is found
    mock_cursor.fetchone.return_value = None
    result = db.fetch_compound_by_name_and_concentration("Nonexistent Compound", 999.0)
    assert result is None

def test_fetch_all_compounds(mocker):
    db = SQLiteDatabase("test.db")
    mock_cursor, _ = mock_database_connection(mocker, db)

    # Expected SQL query for fetching all active compounds
    expected_query = '''
        SELECT compound_name, compound_concentration, coord_x, coord_y
        FROM Compounds
        WHERE is_active = 1
    '''
    # Mock result for fetchall()
    mock_cursor.fetchall.return_value = [
        ("Compound1", 100.0, 50.123, 75.456),
        ("Compound2", 200.0, 60.789, 80.123)
    ]
    
    # Call method
    result = db.fetch_all_compounds()
    
    # Verify that the SQL query was executed with the correct parameters
    verify_sql_query(mock_cursor, expected_query)
    
    # Verify that the result matches the expected list of tuples
    assert result == [
        ("Compound1", 100.0, 50.123, 75.456),
        ("Compound2", 200.0, 60.789, 80.123)
    ]

def test_fetch_all_compounds_colored_by_concentration(mocker):
    db = SQLiteDatabase("test.db")
    mock_cursor, _ = mock_database_connection(mocker, db)

    # Expected SQL query for fetching all active compounds colored by concentration
    expected_query = '''
        SELECT c.compound_name, c.compound_concentration, c.coord_x, c.coord_y, col.R, col.G, col.B
        FROM Compounds c
        INNER JOIN Color_by_concentration col ON c.color_id = col.color_id
        WHERE c.is_active = 1
    '''
    # Mock result for fetchall()
    mock_cursor.fetchall.return_value = [
        ("Compound1", 100.0, 50.123, 75.456, 255, 0, 0),
        ("Compound2", 200.0, 60.789, 80.123, 0, 255, 0)
    ]
    
    # Call method
    result = db.fetch_all_compounds_colored_by_concentration()
    
    # Verify that the SQL query was executed with the correct parameters
    verify_sql_query(mock_cursor, expected_query)
    
    # Verify that the result matches the expected list of tuples
    assert result == [
        ("Compound1", 100.0, 50.123, 75.456, 255, 0, 0),
        ("Compound2", 200.0, 60.789, 80.123, 0, 255, 0)
    ]

def test_fetch_all_compounds_colored_by_moa(mocker):
    db = SQLiteDatabase("test.db")
    mock_cursor, _ = mock_database_connection(mocker, db)

    # Expected SQL query for fetching all active compounds colored by moa
    expected_query = '''
        SELECT c.compound_name, c.compound_concentration, c.coord_x, c.coord_y, col.R, col.G, col.B
        FROM Compounds c
        INNER JOIN Color_by_moa col ON c.moa_id = col.moa_id
        WHERE c.is_active = 1
    '''
    # Mock result for fetchall()
    mock_cursor.fetchall.return_value = [
        ("Compound1", 100.0, 50.123, 75.456, 255, 0, 0),
        ("Compound2", 200.0, 60.789, 80.123, 0, 255, 0)
    ]
    
    # Call method
    result = db.fetch_all_compounds_colored_by_moa()
    
    # Verify that the SQL query was executed with the correct parameters
    verify_sql_query(mock_cursor, expected_query)
    
    # Verify that the result matches the expected list of tuples
    assert result == [
        ("Compound1", 100.0, 50.123, 75.456, 255, 0, 0),
        ("Compound2", 200.0, 60.789, 80.123, 0, 255, 0)
    ]

def test_fetch_compound_details(mocker):
    db = SQLiteDatabase("test.db")
    mock_cursor, _ = mock_database_connection(mocker, db)

    # Expected SQL query for fetching compound details by name and concentration
    expected_query = '''
        SELECT c.smiles, col.moa, col.moa_concentration
        FROM Compounds c
        INNER JOIN Color_by_moa col ON c.moa_id = col.moa_id
        WHERE c.compound_name = ? AND c.compound_concentration = ?
    '''
    # Mock result for fetchone()
    mock_cursor.fetchone.return_value = ("C1=CC=CC=C1", "MOA1", 50.0)
    
    # Call method with sample data
    result = db.fetch_compound_details("Test Compound", 100.0)
    
    # Verify that the SQL query was executed with the correct parameters
    verify_sql_query(mock_cursor, expected_query)
    
    # Verify that the result matches the expected dictionary format
    assert result == ("C1=CC=CC=C1", "MOA1", 50.0)