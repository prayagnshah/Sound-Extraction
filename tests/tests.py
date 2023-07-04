import csv
import pytest
from unittest.mock import patch
import pytest
import os
import datetime
# from src.sound_extraction import get_directories, read_csv_file


# This is your actual code to be tested 
# def get_directories(root_directory):
#     all_files = []
#     directory = []

#     for root, dirs, files in os.walk(root_directory):
#         ext_found = False

#         for file in files:
#             if file.endswith(".flac"):
#                 all_files.append(file)
#                 ext_found = True
#             else:
#                 print(f"File {file} is not a .flac file")

#         if ext_found:
#             directory.append(root)

#     return directory, all_files

# The following is the test case to check the directories and files

# def read_csv_file(csv_file_path, sampleFile, categories_col):
#         """
#         Reads data from a CSV file and filters it based on a column name which has sample audio files and categories column. It returns sample recordings and
#         a dictionary with sample recordings as keys and categories as values.

#         Args:
#             csv_file_path (str): The path to the CSV file to be read.
#             sampleFile (str): The name of the column containing sample audio files.
#             categories_col (str): The name of the column containing categories.

#         Returns:
#             tuple: A tuple containing two elements:
#                 - list: A list of sample recordings.
#                 - dict: A dictionary with sample recordings as keys and categories as values.

#         Steps:
#             1. Open the CSV file and read its content.
#             2. Find the indices of the sampleFile and categories_col columns.
#             3. Extract the relevant data from the CSV file.
#             4. Create a dictionary with sample recordings as keys and categories as values.
#         """
#         with open(csv_file_path, "r") as files:
#             csv_reader = csv.reader(files)

#             header = next(csv_reader)

#             sampleFile_index = header.index(sampleFile)

#             categories_bool = False
#             if categories_col not in header:
#                 print(
#                     "Categories column not found in CSV file, so there is no folder named Nocturnal, Daytime, etc."
#                 )

#                 categories_bool = True

#             else:
#                 categories_index = header.index(categories_col)

#             rows = list(csv_reader)

#         sample_recordings = [row[sampleFile_index] for row in rows]

#         if categories_bool:
#             categories = ["" for row in rows]

#         else:
#             categories = [row[categories_index] for row in rows]

#         categories_dict = {k: v for k, v in zip(sample_recordings, categories)}

#         return sample_recordings, categories_dict
    
    
    
def process_recordings(all_files, sample_recordings):
        """
            Processes long recordings and matches them with the corresponding sample
            recordings based on their timestamps. Returns a dictionary with long
            recordings as keys and lists of associated sample recordings as values.

        Args:
            all_files (list): A list of all long recordings files.
            sample_recordings (list): A list of sample recordings files.

        Returns:
            dict: A dictionary with long recordings as keys and lists of associated
                  sample recordings as values.

        Steps:
            1. Filter and sort long recordings.
            2. Iterate through long recordings and create a dictionary to store the
               associated sample recordings.
            3. Check if a sample recording falls within a long recording's time frame.
            4. Filter the dictionary to remove empty lists and format the keys.
        """

        long_recordings = [file for file in all_files if "T" in file]

        long_recordings.sort()
        recordings_dict = {}

        for long_recording in long_recordings:
            filename, extension = os.path.splitext(long_recording)

            # Putting try and except handling because there will be backup file with .flac and we need to avoid it

            long_start_datetime = datetime.datetime.strptime(filename, "%Y%m%dT%H%M%S")

            try:
                next_long_recording = long_recordings[
                    long_recordings.index(long_recording) + 1
                ]
                next_filename, next_extension = os.path.splitext(next_long_recording)

                duration = (
                    datetime.datetime.strptime(next_filename, "%Y%m%dT%H%M%S")
                    - long_start_datetime
                )

            except IndexError:
                duration = datetime.timedelta(hours=3)

            long_end_datetime = long_start_datetime + duration

            # Create an empty list to hold sample recordings that fall within this long recording's time frame

            recordings_dict[long_start_datetime] = []

            for sample_recording in sample_recordings:
                file, ext = os.path.splitext(sample_recording)

                sample_datetime = datetime.datetime.strptime(file, "%Y%m%d_%H%M%S")

                if long_start_datetime <= sample_datetime <= long_end_datetime:
                    recordings_dict[long_start_datetime].append(sample_recording)

        # Storing the user input for the extension

        extension = ".flac"

        # Removing the empty lists and showing the output with the data which has files in it

        filtered_recordings_dict = {
            key.strftime("%Y%m%dT%H%M%S") + extension: value
            for key, value in recordings_dict.items()
            if value
        }

        return filtered_recordings_dict
    
    
    
def test_get_directories():
    root_dir = '/root'

    # Mock the "os.walk" method
    # Creating directory and then random files in it. 
    with patch.object(os, 'walk') as mock_walk:
        mock_walk.return_value = [
            ('/root', ['dir1', 'dir2'], ['test1.flac', 'test2.txt']),
            ('/root/dir1', [], ['test3.flac', 'test4.jpg']),
            ('/root/dir2', [], ['test5.mp3', 'test6.png', 'test7.flac']),
        ]

        dirs, files = get_directories(root_dir)

        # Checking the flac files and if not then print the file name
        expected_dirs = ['/root', '/root/dir1', '/root/dir2']
        expected_files = ['test1.flac', 'test3.flac', 'test7.flac']

        assert dirs == expected_dirs
        assert files == expected_files


def test_read_csv_file_with_categories_and_sampleFile():
    
    # Create a mock CSV file
    with open('test.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["sampleFile", "category"])
        writer.writerow(["20220506_122345", "Daytime"])
        writer.writerow(["20220506_125621", "Nocturnal"])
        
    # Call the function
    sample_recordings, categories_dict = read_csv_file('test.csv', 'sampleFile', 'category')
    
    # Assert that the function returns the expected output
    assert sample_recordings == ["20220506_122345", "20220506_125621"]
    assert categories_dict == {"20220506_122345": "Daytime", "20220506_125621": "Nocturnal"}
    
    
def test_read_csv_file_without_categories():
    # Create a mock CSV file without categories column
    with open('test.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["sampleFile"])
        writer.writerow(["20220506_122345"])
        writer.writerow(["20220506_125621"])
        
    # Call the function
    sample_recordings, categories_dict = read_csv_file('test.csv', 'sampleFile', 'categories_col')
    
    # Assert that the function returns the expected output
    assert sample_recordings == ["20220506_122345", "20220506_125621"]
    assert categories_dict == {"20220506_122345": "", "20220506_125621": ""}
    
    
def test_read_csv_file_without_data():
    # Create a mock CSV file without data
    with open('test.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["sampleFile", "categories_col"])
        
    # Call the function
    sample_recordings, categories_dict = read_csv_file('test.csv', 'sampleFile', 'categories_col')
    
    # Assert that the function returns the expected output
    assert sample_recordings == []
    assert categories_dict == {}
    
    # Remove the mock CSV file
    os.remove('test.csv')
    
    

def test_process_recordings():
    # Test to check the sample recordings are in the long recordings time frame
    all_files = ["20220506T122345.flac", "20220506T125621.flac", "20220506T130000.flac"]
    sample_recordings = ["20220506_122400.flac", "20220506_125700.flac", "20220506_130100.flac"]
        
    # Call the function
    recordings_dict = process_recordings(all_files, sample_recordings)
    
    # Assert that the function returns the expected output
    assert recordings_dict == {
        "20220506T122345.flac": ["20220506_122400.flac"],
        "20220506T125621.flac": ["20220506_125700.flac"],
        "20220506T130000.flac": ["20220506_130100.flac"],
    }
    