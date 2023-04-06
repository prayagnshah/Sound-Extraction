import os
import datetime
import csv
import soundfile as sf
import numpy as np


def get_directories(root_directory):
    """
    Gets all directories in the root directory and loops through them.
    """
    for root, dirs, files in os.walk(root_directory):
        for directory_path in dirs:

            directory = os.path.join(root, directory_path)

            all_files = os.listdir(directory)

    # print(all_files, directory)
    return directory, all_files


def read_csv_file(csv_file_path, sampleFile):
    """
    Reads data from a CSV file and filters it based on a column name which has sample audio files.
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
    # Filtering in actual recordings

    long_recordings = [file for file in all_files if "T" in file]
    # print(long_recordings)

    recordings_dict = {}

    for long_recording in long_recordings:
        # print(long_recording)

        # Splitting the .flac extension from the filename so datetime can be parsed

        filename, extension = os.path.splitext(long_recording)

        # Get the start and end datetime of the long recording
        # Putting try and except handling because there will be backup file with .flac and we need to avoid it
        try:
            long_start_datetime = datetime.datetime.strptime(
                filename, "%Y%m%dT%H%M%S")
        except ValueError:
            continue

        # Getting the duration of the recording by checking the next long recording's start time and if there is one then,

        try:
            next_long_recording = long_recordings[long_recordings.index(
                long_recording) + 1]
            next_filename, next_extension = os.path.splitext(
                next_long_recording)

            duration = datetime.datetime.strptime(
                next_filename, "%Y%m%dT%H%M%S") - long_start_datetime

        # Assuming the last recording of 3 hours

        except IndexError:

            duration = datetime.timedelta(hours=3)

        long_end_datetime = long_start_datetime + duration

        # Create an empty list to hold sample recordings that fall within this long recording's time frame

        recordings_dict[long_start_datetime] = []

        # Using if condition to check that sample recording falls into long recording
        # Finally producing the output: sample_recording

        for sample_recording in sample_recordings:
            # print(sample_recording)

            file, ext = os.path.splitext(sample_recording)

        # Get the datetime of the sample recording
            sample_datetime = datetime.datetime.strptime(
                file, "%Y%m%d_%H%M%S")

        # Check if the sample recording falls within the current long recording's time frame
            if long_start_datetime <= sample_datetime <= long_end_datetime:
                recordings_dict[long_start_datetime].append(
                    sample_recording)

    # Removing the empty lists and showing the output with the data which has files in it

    filtered_recordings_dict = {
        key.strftime("%Y%m%dT%H%M%S") + ".flac": value for key, value in recordings_dict.items() if value
    }

    return filtered_recordings_dict


def extract_audio_segments(directory, filtered_recordings_dict, output_directory, site_name):

    # Set the duration for the portion of the audio file to extract

    duration = datetime.timedelta(minutes=3)

    recording_keys = sorted(os.listdir(directory))

    # Looping through each key-value pair

    for key, value in filtered_recordings_dict.items():

        # Trying to put in the exception handler if corrupted audio file comes up then it prints in the console and it will still continue the code instead of breaking up

        try:
            # Loading the original audio recording file while samplefile produces array and samplerate together
            audio_file, samplerate = sf.read(os.path.join(directory, key))
        # print(audio_file)
        except Exception as e:
            print(f"Error reading audio file {key}: {e}")
            continue

        # Splitting the key values into datetime

        split_key = os.path.splitext(key)[0]
        # Getting the start time of the audio file from the actual recordings

        start_time_parent = datetime.datetime.strptime(
            split_key, "%Y%m%dT%H%M%S")

        # Loop through each specified snippet in the value

        for snippet in value:
            start_time_str = os.path.splitext(snippet)[0]
            # print(start_time_str)

            # Extract the start and end time for the snippet and parsing string as datetime object

            start_time = datetime.datetime.strptime(
                start_time_str, "%Y%m%d_%H%M%S")

            # Getting the actual start time of the snippet in the audio file

            snippet_start_time = start_time - start_time_parent

            # Calculate the start and end frame indices for the portion of the audio file to extract into seconds

            start_frame = int(
                snippet_start_time.total_seconds() * samplerate)
            end_frame = int(
                (snippet_start_time + duration).total_seconds() * samplerate)

            # Checking the index of the current key

            current_key_index = recording_keys.index(key)

            # Due to the fact that the audio files are not of 3 mins duration so we need to check if the duration is less than 3 mins then we need to add the next audio file to it

            if current_key_index + 1 < len(recording_keys):

                # According to the flac recorders, proper recording are not captured so using 3 mins 6 seconds to get 3 mins extraction

                duration_new = datetime.timedelta(minutes=3, seconds=6)

                next_key = recording_keys[current_key_index + 1]

                next_key_start_time = datetime.datetime.strptime(
                    os.path.splitext(next_key)[0], "%Y%m%dT%H%M%S")

                # Checking if the duration of the snippet is greater than the next key's start time

                if start_time + duration_new > next_key_start_time:
                    time_duration = next_key_start_time - start_time

                    # Loading the next audio file

                    next_audio_file, next_samplerate = sf.read(
                        os.path.join(directory, next_key))

                    # Getting the remaining duration of the snippet

                    remaining_duration = duration_new - time_duration

                    # Getting the remaining audio from the next audio file

                    remaining_audio = next_audio_file[:int(
                        remaining_duration.total_seconds() * next_samplerate)]

                    # Concatenating the audio files

                    snippet_data = np.concatenate((
                        audio_file[start_frame:], remaining_audio))
                    # print(remaining_audio)
                    # snippet_data = audio_file[start_frame:] + resampled_remaining_audio   # nopep8
                    # print(snippet_data)

                else:
                    snippet_data = audio_file[start_frame:end_frame]

            else:
                # Extract the portion of the audio data using numpy array indexing because soundfile data comes in integers

                snippet_data = audio_file[start_frame:end_frame]

            # Write the extracted audio data to a new file

            output_filename = os.path.splitext(snippet)[0] + '.flac'

            # Writing the new audio of 3 mins to the desired directory
            export_segment = sf.write(os.path.join(output_directory, site_name + output_filename),
                                      snippet_data, samplerate)

    return export_segment, output_directory


# Getting the root directory and output directory from the user

root_directory = "C:\\Users\\ShahP\\Documents\\extract-audio-files"
output_directory = "C:\\Users\\ShahP\\Documents\\extract-audio-files"
site_name = "WolfesIsland698161"
csv_file_path = "C:\\Users\\ShahP\\Downloads\\bossSampleTest.csv"

# Calling the functions

directory, all_files = get_directories(root_directory)
sampleFile = "sampleFile"
sample_recordings = read_csv_file(csv_file_path, sampleFile)

filtered_recordings_dict = process_recordings(
    directory, all_files, sample_recordings)
# print(filtered_recordings_dict)

export_segment, output_directory = extract_audio_segments(
    directory, filtered_recordings_dict, output_directory, site_name)
