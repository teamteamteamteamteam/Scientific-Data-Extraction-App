import sqlite3
import pytest

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.utils.DatabaseCreator import DatabaseCreator

@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    dbCreator = DatabaseCreator()
    dbCreator.conn = conn
    dbCreator.cursor = cursor
    yield dbCreator

    conn.close()

def createTableCompoundsTest(db):
    db.createTableCompounds()

    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Compounds';")
    table = db.cursor.fetchone()
    assert table is not None, "Compounds table has not been created."


def createTableImagesTest(db):
    db.createTableImages()
    
    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Images';")
    table = db.cursor.fetchone()
    assert table is not None, "Images table has not been created."