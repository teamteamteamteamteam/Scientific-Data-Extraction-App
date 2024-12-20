from pathlib import Path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.utils.UsablePaths import Paths

def test_database_path():
    # Check if the database path is set correctly
    expected_path = Path.cwd() / 'backend' / 'database' / 'database.db'
    assert Paths.DATABASE_PATH == expected_path

def test_compound_csv_path():
    # Check if the path to the chemical compound CSV file is correct
    expected_path = Path.cwd() / 'backend' / 'resources' / 'BBBC021_v1_compound.csv'
    assert Paths.COMPOUND_CSV_PATH == expected_path

def test_images_csv_path():
    # Check if the path to the images CSV file is correct
    expected_path = Path.cwd() / 'backend' / 'resources' / 'BBBC021_v1_image.csv'
    assert Paths.IMAGES_CSV_PATH == expected_path