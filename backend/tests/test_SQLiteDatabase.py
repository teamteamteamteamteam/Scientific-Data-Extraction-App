import unittest
import pytest
from unittest.mock import MagicMock, patch
from unittest import mock
import textwrap
from sqlite3 import Connection, Cursor
import sys
import os
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.utils.SQLiteDatabase import SQLiteDatabase
from backend.utils.UsablePaths import Paths

# Funkcja pomocnicza do mockowania połączenia i kursora
def mock_db_connection(mocker, db):
    mock_cursor = mock.MagicMock()
    mock_connection = mock.MagicMock()
    db.connection = mock_connection
    db.cursor = mock_cursor
    mocker.patch.object(db, 'connect', return_value=None)
    db.connect()  # Bez faktycznego połączenia
    return mock_cursor, mock_connection

# Funkcja pomocnicza do sprawdzania zapytań SQL
def check_sql_query(mock_cursor, expected_query):
    cleaned_expected_query = ''.join(expected_query.split())
    cleaned_actual_query = ''.join(mock_cursor.execute.call_args[0][0].split())
    assert cleaned_expected_query == cleaned_actual_query, f"Expected: {cleaned_expected_query}, but got: {cleaned_actual_query}"

# Funkcja pomocnicza do normalizacji zapytań
def normalize_query(query):
    return textwrap.dedent(query).strip()

# Test dla singletona
def test_singleton():
    db1 = SQLiteDatabase("test.db")
    db2 = SQLiteDatabase("test.db")
    assert db1 is db2

# Test dla connect()
def test_connect(mocker):
    db = SQLiteDatabase("test.db")
    mock_connect = mocker.patch('sqlite3.connect')
    db.connect()
    mock_connect.assert_called_once_with("test.db")
    assert db.conn is not None

# Test dla close()
def test_close(mocker):
    # Mockowanie połączenia i kursora
    mock_cursor = MagicMock()
    mock_conn = MagicMock()

    db = SQLiteDatabase("test.db")
    
    # Ustawienie conn i cursor przed wywołaniem connect()
    db.conn = mock_conn
    db.cursor = mock_cursor

    # Uruchomienie testu
    db.connect()  # Connect nie ustawi conn, ponieważ jest już mockowane

    # Sprawdzamy, czy kursor i połączenie zostały zamknięte
    db.close()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


# Test dla create_table_compounds()
def test_create_table_compounds(mocker):
    db = SQLiteDatabase("test.db")
    mock_cursor, _ = mock_db_connection(mocker, db)

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
    check_sql_query(mock_cursor, expected_query)

# Test dla create_table_images()
def test_create_table_images(mocker):
    db = SQLiteDatabase("test.db")
    mock_cursor, _ = mock_db_connection(mocker, db)

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
    check_sql_query(mock_cursor, expected_query)

# Test dla create_table_color_by_concentration()
def test_create_table_color_by_concentration(mocker):
    db = SQLiteDatabase("test.db")
    mock_cursor, _ = mock_db_connection(mocker, db)

    expected_query = '''
        CREATE TABLE IF NOT EXISTS Color_by_concentration (
            color_id INTEGER PRIMARY KEY AUTOINCREMENT,
            R REAL,
            G REAL,
            B REAL    
        )
    '''
    db.create_table_color_by_concentration()
    check_sql_query(mock_cursor, expected_query)

# Test dla create_table_color_by_moa()
def test_create_table_color_by_moa(mocker):
    db = SQLiteDatabase("test.db")
    mock_cursor, _ = mock_db_connection(mocker, db)

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
    check_sql_query(mock_cursor, expected_query)

# Test dla insert_into_table_compounds()
def test_insert_into_table_compounds(mocker):
    db = SQLiteDatabase("test.db")
    mock_cursor, _ = mock_db_connection(mocker, db)

    expected_query = '''
        INSERT INTO Compounds (compound_name, compound_concentration, smiles, is_active)
        VALUES (?, ?, ?, ?)
    '''
    db.insert_into_table_compounds("Test Compound", 10.0, "C1=CC=CC=C1", 1)
    check_sql_query(mock_cursor, expected_query)

# Możesz dodać inne testy w podobny sposób.
