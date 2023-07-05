import csv
from unittest.mock import patch
import os
from src.tests.sound_extraction_tests import get_directories, read_csv_file, process_recordings


def test_get_directories():
    root_dir = "/root"

    # Mock the "os.walk" method
    # Creating directory and then random files in it.
    with patch.object(os, "walk") as mock_walk:
        mock_walk.return_value = [
            ("/root", ["dir1", "dir2"], ["test1.flac", "test2.txt"]),
            ("/root/dir1", [], ["test3.flac", "test4.jpg"]),
            ("/root/dir2", [], ["test5.mp3", "test6.png", "test7.flac"]),
        ]

        dirs, files = get_directories(root_dir)

        # Checking the flac files and if not then print the file name
        expected_dirs = ["/root", "/root/dir1", "/root/dir2"]
        expected_files = ["test1.flac", "test3.flac", "test7.flac"]

        assert dirs == expected_dirs
        assert files == expected_files


def test_read_csv_file_with_categories_and_sampleFile():
    # Create a mock CSV file
    with open("test.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["sampleFile", "category"])
        writer.writerow(["20220506_122345", "Daytime"])
        writer.writerow(["20220506_125621", "Nocturnal"])

    # Call the function
    sample_recordings, categories_dict = read_csv_file(
        "test.csv", "sampleFile", "category"
    )

    # Assert that the function returns the expected output
    assert sample_recordings == ["20220506_122345", "20220506_125621"]
    assert categories_dict == {
        "20220506_122345": "Daytime",
        "20220506_125621": "Nocturnal",
    }


def test_read_csv_file_without_categories():
    # Create a mock CSV file without categories column
    with open("test.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["sampleFile"])
        writer.writerow(["20220506_122345"])
        writer.writerow(["20220506_125621"])

    # Call the function
    sample_recordings, categories_dict = read_csv_file(
        "test.csv", "sampleFile", "categories_col"
    )

    # Assert that the function returns the expected output
    assert sample_recordings == ["20220506_122345", "20220506_125621"]
    assert categories_dict == {"20220506_122345": "", "20220506_125621": ""}


def test_read_csv_file_without_data():
    # Create a mock CSV file without data
    with open("test.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["sampleFile", "categories_col"])

    # Call the function
    sample_recordings, categories_dict = read_csv_file(
        "test.csv", "sampleFile", "categories_col"
    )

    # Assert that the function returns the expected output
    assert sample_recordings == []
    assert categories_dict == {}

    # Remove the mock CSV file
    os.remove("test.csv")


def test_process_recordings():
    # Test to check the sample recordings are in the long recordings time frame
    all_files = ["20220506T122345.flac", "20220506T125621.flac", "20220506T130000.flac"]
    sample_recordings = [
        "20220506_122400.flac",
        "20220506_125700.flac",
        "20220506_130100.flac",
        "20220506_130200.flac",
    ]

    # Call the function
    recordings_dict = process_recordings(all_files, sample_recordings)

    # Assert that the function returns the expected output
    assert recordings_dict == {
        "20220506T122345.flac": ["20220506_122400.flac"],
        "20220506T125621.flac": ["20220506_125700.flac"],
        "20220506T130000.flac": ["20220506_130100.flac", "20220506_130200.flac"],
    }


def test_process_recordings_without_matches():
    # Testing the sample recordings which are not in the long recordings time frame
    all_files = ["20220506T122345.flac", "20220506T125621.flac", "20220506T130000.flac"]
    sample_recordings = [
        "20220507_120000.flac",
        "20220507_121500.flac",
        "20220507_123000.flac",
    ]

    # Call the function
    recordings_dict = process_recordings(all_files, sample_recordings)

    # Assert that the function returns the expected output
    assert recordings_dict == {}
