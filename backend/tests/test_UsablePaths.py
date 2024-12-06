import sys
import os

current = os.path.dirname(os.path.realpath(__file__)) # Get the current file directory
parent = os.path.dirname(current) # Get the parent directory of the current directory
sys.path.append(parent) # Add the parent directory to sys.path

import UsablePaths
import pytest
from pathlib import Path

def test_database_path():
    # Check if the database path is set correctly
    expected_path = Path.cwd() / 'backend' / 'database' / 'database.db'
    assert UsablePaths.Paths.DATABASE_PATH == expected_path

def test_compound_csv_path():
    # Check if the path to the chemical compound CSV file is correct
    expected_path = Path.cwd() / 'backend' / 'resources' / 'BBBC021_v1_compound.csv'
    assert UsablePaths.Paths.COMPOUND_CSV_PATH == expected_path

def test_images_csv_path():
    # Check if the path to the images CSV file is correct
    expected_path = Path.cwd() / 'backend' / 'resources' / 'BBBC021_v1_image.csv'
    assert UsablePaths.Paths.IMAGES_CSV_PATH == expected_path