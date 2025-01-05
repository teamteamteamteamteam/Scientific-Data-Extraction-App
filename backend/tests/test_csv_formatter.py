from pathlib import Path
import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.formatter_csv.formatt_csv_files import CsvFormatter, COLS_TO_SKIP


class TestFormatter(unittest.TestCase):

    def test_modify_file_path(self):
        formatter = CsvFormatter("original", "formatted")
        result = formatter.modify_file_path("original/example.csv")
        expected = "formatted/example_formatted.csv"
        self.assertEqual(result, expected)


    def test_modify_file_path_rising_error(self):
        formatter = CsvFormatter("random_name", "formatted")
        with self.assertRaises(FileNotFoundError):
            formatter.modify_file_path("original/example.csv")
        

    @patch("pathlib.Path.mkdir")
    def test_create_folder(self, mock_mkdir):
        formatter = CsvFormatter("input", "output")
        result = formatter.create_folder("new_folder")
        expected = Path("output/new_folder")
        self.assertEqual(result, expected)
        mock_mkdir.assert_called_once_with(exist_ok=True)


    @patch("os.walk")
    @patch.object(CsvFormatter, "create_folder")
    def test_get_csv_files(self, mock_create_folder, mock_os_walk):

        mock_os_walk.return_value = [
            ("input", ["folder1", "folder2"], ["file1.csv", "file2.txt"]),
            ("input/folder1", [], ["file3.csv"]),
            ("input/folder2", [], ["file4.csv", "file5.txt"])
        ]
        
        formatter = CsvFormatter("input", "output")
        result = formatter.get_csv_files()
        expected = [
            str(Path("input") / "file1.csv"),
            str(Path("input/folder1") / "file3.csv"),
            str(Path("input/folder2") / "file4.csv")
        ]
        
        self.assertEqual([os.path.normpath(path) for path in result], [os.path.normpath(path) for path in expected])
        mock_create_folder.assert_any_call("folder1")
        mock_create_folder.assert_any_call("folder2")
        self.assertEqual(mock_create_folder.call_count, 2)


    @patch("os.makedirs")
    @patch.object(CsvFormatter, "get_csv_files")
    @patch.object(CsvFormatter, "_CsvFormatter__delete_some_colls_in_csv")
    @patch.object(CsvFormatter, "modify_file_path")
    def test_run_formatter_delete_call_count(self, mock_modify_file_path, mock_delete, mock_get_csv_files, mock_makedirs):
        mock_get_csv_files.return_value = [
            "input/file1.csv",
            "input/folder1/file2.csv",
            "input/Image_file.csv"
        ]
        mock_modify_file_path.return_value = "output/file1_formatted.csv"
        formatter = CsvFormatter("input", "output")
        formatter.run_formatter()
        self.assertEqual(mock_delete.call_count, 2)
