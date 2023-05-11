import os
import datetime
import csv
import soundfile as sf
import numpy as np
import argparse


def get_directories(root_directory):
    """
    Gets all directories in the root directory and loops through them.
    It will only accept the file which are in the .wav or .flac format.
    """
    all_files = []
    directory = []

    for root, dirs, files in os.walk(root_directory):
        for directory_path in dirs:

            directory_in = os.path.join(root, directory_path)
            directory.append(directory_in)

            for file in os.listdir(directory_in):
                if file.endswith(args.extension):
                    all_files.append(file)

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


def process_recordings(all_files, sample_recordings):
    # Filtering in actual recordings

    long_recordings = [
        file for file in all_files if "T" in file]

    long_recordings.sort()
    recordings_dict = {}

    for long_recording in long_recordings:

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

    # Storing the user input for the extension

    extension = args.extension

    # Removing the empty lists and showing the output with the data which has files in it

    filtered_recordings_dict = {
        key.strftime("%Y%m%dT%H%M%S") + extension: value for key, value in recordings_dict.items() if value
    }

    return filtered_recordings_dict


def extract_audio_segments(filtered_recordings_dict, output_directory, site_name):

    # Set the duration for the portion of the audio file to extract

    duration = datetime.timedelta(minutes=args.duration)

    # Calling the function to get the directories

    directories, all_files = get_directories(root_directory)

    for directory in directories:

        # Calling the function to get the original audio files

        recording_keys = sorted(os.listdir(directory))

        # Looping through each key-value pair

        for key, value in filtered_recordings_dict.items():

            # Checking if the key is in the original audio files

            if key not in recording_keys:
                continue

            # Trying to put in the exception handler if corrupted audio file comes up then it prints in the console and it will still continue the code instead of breaking up

            try:
                # Loading the original audio recording file while samplefile produces array and samplerate together

                audio_file, samplerate = sf.read(os.path.join(directory, key))

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

                    # Checking the extension of the audio file and adding the seconds accordingly

                    if args.extension == ".flac":
                        seconds = 6
                    elif args.extension == ".wav":
                        seconds = 1
                    else:
                        pass

                    # According to the flac recorders, proper recording are not captured so using 3 mins 6 seconds to get 3 mins extraction

                    duration_new = datetime.timedelta(minutes=args.duration, seconds=seconds)  # nopep8

                    next_key = recording_keys[current_key_index + 1]

                    next_key_start_time = datetime.datetime.strptime(
                        os.path.splitext(next_key)[0], "%Y%m%dT%H%M%S")

                    # Checking if the duration of the snippet is greater than the next key's start time and flag "-span" is used then it won't concatenate the audio files

                    if not args.span and start_time + duration_new > next_key_start_time:
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

                    else:
                        snippet_data = audio_file[start_frame:end_frame]

                else:
                    # Extract the portion of the audio data using numpy array indexing because soundfile data comes in integers

                    snippet_data = audio_file[start_frame:end_frame]

                # Storing the user input for the extension

                extension = args.extension

                # Write the extracted audio data to a new file

                output_filename = os.path.splitext(snippet)[0] + extension

                # Writing the new audio of 3 mins to the desired directory

                export_segment = sf.write(os.path.join(output_directory, site_name + output_filename),
                                          snippet_data, samplerate)

    return export_segment, output_directory


def process_audio_files(directory, slice_duration, output_directory):

    # Traversing the directories and files in the directory

    for root, dirs, files in os.walk(directory):

        # Looping the files of that directory

        for file in files:
            file_str = os.path.splitext(file)[0]
            file_datetime = datetime.datetime.strptime(
                file_str, "%Y%m%dT%H%M%S")

            audio, sample_rate = sf.read(os.path.join(root, file))

            # total samples in the audio file

            total_samples = len(audio)

            # samples in each chunk

            chunk_samples = int(slice_duration * sample_rate)

            start = 0

            for i in range(0, total_samples, chunk_samples):
                chunk = audio[i:i + chunk_samples]

                # Getting the start time of the audio file from the actual recordings and adding the chunk duration

                recording_time = (
                    file_datetime + datetime.timedelta(seconds=start)).strftime("%Y%m%dT%H%M%S")

                filename = os.path.join(
                    output_directory, "{}.wav".format(recording_time))

                sf.write(filename, chunk, sample_rate)

                start += slice_duration


# Create an ArgumentParser object
parser = argparse.ArgumentParser(
    description='A program that will help to extract recording from the actual long recordings.')

parser.add_argument('-r', '--root_directory', type=str, required=True, help='The root directory of the long recordings')  # nopep8
parser.add_argument('-o', '--output_directory', type=str, help='The output directory to store the extracted audio segments')  # nopep8
parser.add_argument('-c', '--csv_file_path', type=str, help='The path of the csv file')  # nopep8
parser.add_argument('-d', '--duration', type=int, default=3, help='What duration of extracted segments you want?')  # nopep8
parser.add_argument('-s', '--site_name', type=str,  help='The name of the site')  # nopep8
parser.add_argument('-span', '--span', action='store_true', help='Extract original files instead of spanning')  # nopep8
parser.add_argument('-e', '--extension', type=str, choices=['.wav', '.flac'], default='.flac', help='The extension of the original audio files')  # nopep8
parser.add_argument('-slice', '--slice', type=int, help='In how many seconds you want to slice the audio files?')  # nopep8
# Parse the command line arguments

args = parser.parse_args()

# Getting the root directory and output directory from the user

root_directory = args.root_directory
output_directory = args.output_directory
site_name = args.site_name
csv_file_path = args.csv_file_path

# If user uses slice to get divide audio files into same length then only function will be activated

if args.slice:
    directory = root_directory
    slice_duration = args.slice
    process_audio_files(directory, slice_duration, output_directory)

# If user wants to extract the audio files from sample time frame this statement will be executed

else:

    # Calling the functions

    directory, all_files = get_directories(root_directory)

    sampleFile = "sampleFile"
    sample_recordings = read_csv_file(csv_file_path, sampleFile)

    filtered_recordings_dict = process_recordings(all_files, sample_recordings)

    export_segment, output_directory = extract_audio_segments(
        filtered_recordings_dict, output_directory, site_name)


# filename
# test cases
