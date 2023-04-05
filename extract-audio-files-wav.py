import os
import csv
from datetime import datetime, timedelta
from pydub import AudioSegment
import argparse


def get_directories(root_directory):
    """
    Gets all directories in the root directory and loops through them.
    """
    for root, dirs, files in os.walk(root_directory):
        for directory_path in dirs:

            directory = os.path.join(root, directory_path)

            all_files = os.listdir(directory)

    return directory, all_files


def read_csv_file(csv_file_path, sampleFile):
    """
    Reads data from a CSV file and filters it based on a column name of sample audio.
    """
    with open(csv_file_path, 'r') as files:

        # Creating the csv object

        csv_reader = csv.reader(files)

        # Reading the header row

        header = next(csv_reader)

        # Finding the index column

        sampleFile_index = header.index(sampleFile)

        # storing the values in list so that it can be used once the file is closed

        rows = list(csv_reader)

    # Filtering the sample recordings

    sample_recordings = [row[sampleFile_index] for row in rows]
    # print(sample_recordings)

    return sample_recordings


def process_recordings(directory, all_files, sample_recordings):
    """
    Processes long recordings and filters sample recordings to find out the samples in each long recording.
    """
    long_recordings = [file for file in all_files if "T" in file]  # nopep8
    # print(long_recordings)
    long_recordings.sort()
    recordings_dict = {}

    for long_recording in long_recordings:
        filename, extension = os.path.splitext(long_recording)
        long_start_datetime = datetime.strptime(
            filename, "%Y%m%dT%H%M%S")

        try:
            next_long_recording = long_recordings[long_recordings.index(
                long_recording) + 1]
            next_filename, next_extension = os.path.splitext(
                next_long_recording)
            duration = datetime.strptime(
                next_filename, "%Y%m%dT%H%M%S") - long_start_datetime
        except IndexError:
            duration = timedelta(hours=3)

        long_end_datetime = long_start_datetime + duration
        recordings_dict[long_start_datetime] = []

        for sample_recording in sample_recordings:
            file, ext = os.path.splitext(sample_recording)
            sample_datetime = datetime.strptime(
                file, "%Y%m%d_%H%M%S")

            if long_start_datetime <= sample_datetime <= long_end_datetime:
                recordings_dict[long_start_datetime].append(
                    sample_recording)

    # Filtering the recordings dictionary to remove empty values

    filtered_recordings_dict = {
        key.strftime("%Y%m%dT%H%M%S") + ".wav": value for key, value in recordings_dict.items() if value
    }

    return filtered_recordings_dict


def extract_audio_segments(directory, filtered_recordings_dict, output_directory, site_name):

    # Sorting the original recordings in ascending order

    recording_keys = sorted(os.listdir(directory))

    # Creating a list to store the audio segments and the file paths

    file_paths = []
    audio_segments = []

    for key, value in filtered_recordings_dict.items():
        # Loading the 3-hour audio recording file
        audio_file = AudioSegment.from_wav(os.path.join(directory, key))

        # Splitting the key values into datetime
        split_key = os.path.splitext(key)[0]

        # Loop through each specified snippet in the value
        for snippet in value:
            start_time_str = os.path.splitext(snippet)[0]

            # Extract the start and end time for the snippet and parsing string as datetime object
            start_time = datetime.strptime(start_time_str, "%Y%m%d_%H%M%S")

            # Getting the start time of the audio file from the actual recordings
            start_time_parent = datetime.strptime(split_key, "%Y%m%dT%H%M%S")

            # Getting the actual start time of the snippet in the audio file
            snippet_start_time = start_time - start_time_parent

            # Converting into milliseconds as Audio segment accepts only ms
            snippet_start_time_ms = snippet_start_time.total_seconds() * 1000

            # Trying to get the snippet's end time from actual recording
            snippet_end_time = snippet_start_time + timedelta(minutes=3)

            # Converting the end time of the snippet into milliseconds
            snippet_end_time_ms = snippet_end_time.total_seconds() * 1000

            # Extracting the index of the current key from the list of original recording keys
            current_key_index = recording_keys.index(key)

            # Checking the condition if the snippet's end time is beyond the end of the current recording file
            if current_key_index + 1 < len(recording_keys):
                # Find the next key from the list of original recording keys
                next_key = recording_keys[current_key_index + 1]

                # Checking the length of the parent recording file
                length_parent_snippet = len(audio_file)

                # Check if the snippet time is beyond the end of current recording file
                if snippet_end_time_ms > length_parent_snippet:
                    next_audio_file = AudioSegment.from_wav(
                        os.path.join(directory, next_key))
                    remaining_time_ms = snippet_end_time_ms - length_parent_snippet + 1
                    remaining_audio = next_audio_file[:int(remaining_time_ms)]
                    three_minute_audio = audio_file[snippet_start_time_ms:] + \
                        remaining_audio

                else:
                    three_minute_audio = audio_file[snippet_start_time_ms:snippet_end_time_ms]

            else:
                three_minute_audio = audio_file[snippet_start_time_ms:snippet_end_time_ms]

            # Exporting the audio segment to a wav file

            output_path = os.path.join(
                output_directory, "{}_{}.wav".format(site_name, start_time_str))
            three_minute_audio.export(output_path, format="wav")

            # Appending the audio segment and the output path to the list

            audio_segments.append(three_minute_audio)
            file_paths.append(output_path)

    return audio_segments, file_paths, output_directory


# # Create an ArgumentParser object
# parser = argparse.ArgumentParser(
#     description='A program that will help to extract recording from the actual long recordings.')

# parser.add_argument('-r', '--root_directory', type=str, required=True, help='The root directory of the long recordings')  # nopep8
# parser.add_argument('-o', '--output_directory', type=str, required=True, help='The output directory to store the extracted audio segments')  # nopep8
# parser.add_argument('-c', '--csv_file_path', type=str, required=True, help='The path of the csv file')  # nopep8
# parser.add_argument('-d', '--duration', type=int, help='The duration of the audio segment in minutes')  # nopep8

# # Parse the command line arguments
# args = parser.parse_args()


# Getting the directories and files
root_directory = "C:\\Users\\ShahP\\Documents\\extract-audio-files"
output_directory = "C:\\Users\\ShahP\\Documents\\extract-audio-files"
site_name = "PortLHebert527829"
directory, all_files = get_directories(root_directory)

# Reading the csv file and can change the column name to read the sample recordings

csv_file_path = "C:\\Users\\ShahP\\Downloads\\bossSampleTest.csv"
sampleFile = "sampleFile"
sample_recordings = read_csv_file(csv_file_path, sampleFile)

# Processing the recordings to find out the samples in each long recording

filtered_recordings_dict = process_recordings(
    directory, all_files, sample_recordings)

# Extracting the audio segments from the long recordings

audio_segments, file_paths, output_directory = extract_audio_segments(
    directory, filtered_recordings_dict, output_directory, site_name)
