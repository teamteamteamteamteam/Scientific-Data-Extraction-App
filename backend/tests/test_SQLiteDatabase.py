import unittest
import pytest
from unittest.mock import MagicMock, patch
from unittest import mock
import textwrap
import sqlite3
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

# Test dla sytuacji, gdy sqlite3.connect rzuca wyjątek
def test_connect_raises_runtime_error(mocker):
    db = SQLiteDatabase("test.db")
    db.conn = None  # Wyraźnie ustaw początkowy stan `conn` na `None`

    # Mockowanie sqlite3.connect, aby rzucało wyjątek sqlite3.Error
    mocker.patch('sqlite3.connect', side_effect=sqlite3.Error("Mocked connection error"))

    # Sprawdzenie, czy metoda connect() rzuca odpowiedni RuntimeError
    with pytest.raises(RuntimeError, match="Failed to connect to the database: Mocked connection error"):
        db.connect()

    # Upewnienie się, że `db.conn` nadal jest `None` po wyjątku
    assert db.conn is None




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

def test_commit_success(mocker):
    # Mockowanie połączenia
    mock_conn = MagicMock()
    db = SQLiteDatabase("test.db")
    db.conn = mock_conn  # Ustawienie aktywnego połączenia

    # Wywołanie commit
    db.commit()

    # Sprawdzamy, czy `commit` został wywołany
    mock_conn.commit.assert_called_once()

def test_commit_raises_runtime_error_on_commit_failure(mocker):
    # Mockowanie połączenia, aby rzucało wyjątek podczas `commit`
    mock_conn = MagicMock()
    mock_conn.commit.side_effect = sqlite3.Error("Mocked commit error")
    db = SQLiteDatabase("test.db")
    db.conn = mock_conn  # Ustawienie aktywnego połączenia

    # Sprawdzamy, czy metoda rzuca `RuntimeError` z odpowiednim komunikatem
    with pytest.raises(RuntimeError, match="Error during transaction commit: Mocked commit error"):
        db.commit()

def test_commit_raises_runtime_error_no_connection():
    db = SQLiteDatabase("test.db")
    db.conn = None  # Brak aktywnego połączenia

    # Sprawdzamy, czy metoda rzuca `RuntimeError` z odpowiednim komunikatem
    with pytest.raises(RuntimeError, match="No active database connection."):
        db.commit()


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

# Test dla create_table_compounds w przypadku błędu
def test_create_table_compounds_raises_error(mocker, capsys):
    db = SQLiteDatabase("test.db")
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = sqlite3.Error("Mocked error creating Compounds table")
    db.cursor = mock_cursor

    # Uruchomienie metody
    db.create_table_compounds()

    # Przechwycenie wyjścia
    captured = capsys.readouterr()

    # Sprawdzenie, czy komunikat o błędzie pojawił się w standardowym wyjściu
    assert "Error creating Compounds table: Mocked error creating Compounds table" in captured.out

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

# Test dla create_table_images w przypadku błędu
def test_create_table_images_raises_error(mocker, capsys):
    db = SQLiteDatabase("test.db")
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = sqlite3.Error("Mocked error creating Images table")
    db.cursor = mock_cursor

    # Uruchomienie metody
    db.create_table_images()

    # Przechwycenie wyjścia
    captured = capsys.readouterr()

    # Sprawdzenie, czy komunikat o błędzie pojawił się w standardowym wyjściu
    assert "Error creating Images table: Mocked error creating Images table" in captured.out

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

# Test dla create_table_color_by_concentration w przypadku błędu
def test_create_table_color_by_concentration_raises_error(mocker, capsys):
    db = SQLiteDatabase("test.db")
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = sqlite3.Error("Mocked error creating Color_by_concentration table")
    db.cursor = mock_cursor

    # Uruchomienie metody
    db.create_table_color_by_concentration()

    # Przechwycenie wyjścia
    captured = capsys.readouterr()

    # Sprawdzenie, czy komunikat o błędzie pojawił się w standardowym wyjściu
    assert "Error creating Color_by_concentration table: Mocked error creating Color_by_concentration table" in captured.out


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

# Test dla create_table_color_by_moa w przypadku błędu
def test_create_table_color_by_moa_raises_error(mocker, capsys):
    db = SQLiteDatabase("test.db")
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = sqlite3.Error("Mocked error creating Color_by_moa table")
    db.cursor = mock_cursor

    # Uruchomienie metody
    db.create_table_color_by_moa()

    # Przechwycenie wyjścia
    captured = capsys.readouterr()

    # Sprawdzenie, czy komunikat o błędzie pojawił się w standardowym wyjściu
    assert "Error creating Color_by_moa table: Mocked error creating Color_by_moa table" in captured.out


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

# Test dla update_compounds_moa
def test_update_compounds_moa(mocker):
    db = SQLiteDatabase("test.db")
    mock_cursor, _ = mock_db_connection(mocker, db)

    expected_query = '''
        UPDATE Compounds 
        SET moa_id = ?
        WHERE compound_name = ?
    '''
    db.update_compounds_moa("Test Compound", 123)
    check_sql_query(mock_cursor, expected_query)

# Test dla update_compound_coordinates
def test_update_compound_coordinates(mocker):
    db = SQLiteDatabase("test.db")
    mock_cursor, _ = mock_db_connection(mocker, db)

    expected_query = '''
        UPDATE Compounds 
        SET coord_x = ?, coord_y = ?, is_active = ?
        WHERE compound_id = ?
    '''
    db.update_compound_coordinates(1, "100.123", "200.456", 1)
    check_sql_query(mock_cursor, expected_query)

# Test dla updata_compounds_empty_moa
def test_updata_compounds_empty_moa(mocker):
    db = SQLiteDatabase("test.db")
    mock_cursor, _ = mock_db_connection(mocker, db)

    expected_query = '''
        UPDATE Compounds 
        SET moa_id = ?
        WHERE moa_id IS NULL
    '''
    db.updata_compounds_empty_moa(123)
    check_sql_query(mock_cursor, expected_query)

