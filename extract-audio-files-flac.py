import os
import datetime
import csv
import soundfile as sf


# Getting all the files in the directory
# Trying to establish that we can use multiple directories at once

directories = [
    "D:\\wolfesIsland\\2439985\\SD1\\soundFiles\\20220603_wolfesIsland"]

# Looping the files of that directory

for directory in directories:

    # Setting up the exception handler if directory path is wrong still the code will keep moving
    # In console we will be able to get to know which directory was corrupt
    try:
        all_files = os.listdir(directory)
    except FileNotFoundError as e:
        print(
            f"Directory path {directory} not found. Skipping this directory...")
        continue

    # print(all_files)

    with open('D:\\wolfesIsland\\2439985\\sampleSchedule\\WolfesIsland2439985_RecordingDraw.csv', 'r') as files:

        # Creating the csv object

        csv_reader = csv.reader(files)

        # Reading the header row

        header = next(csv_reader)

        # Finding the index column

        sampleFile_index = header.index('sampleFile')

        # storing the values in list so that it can be used once the file is closed

        rows = list(csv_reader)

    # Filtering the sample recordings

    sample_recordings = [row[sampleFile_index] for row in rows]
    # print(sample_recordings)

    # Filtering in actual recordings

    long_recordings = [file for file in all_files if "T" in file]
    # print(long_recordings)

    recordings_dict = {}

    for long_recording in long_recordings:
        # print(long_recording)

        # Splitting the .wav extension from the filename so datetime can be parsed

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
                recordings_dict[long_start_datetime].append(sample_recording)

    # Removing the empty lists and showing the output with the data which has files in it

    filtered_recordings_dict = {
        key.strftime("%Y%m%dT%H%M%S") + ".flac": value for key, value in recordings_dict.items() if value
    }

    # print(filtered_recordings_dict)

    # Set the duration for the portion of the audio file to extract
    duration = datetime.timedelta(minutes=3)

    # Looping through each key-value pair

    for key, value in filtered_recordings_dict.items():

        # Loading the original audio recording file while samplefile produces array and samplerate together
        audio_file, samplerate = sf.read(os.path.join(directory, key))
        # print(audio_file)

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

            start_frame = int(snippet_start_time.total_seconds() * samplerate)
            end_frame = int(
                (snippet_start_time + duration).total_seconds() * samplerate)

            # Extract the portion of the audio data using numpy array indexing because soundfile data comes in integers

            snippet_data = audio_file[start_frame:end_frame]

            # Write the extracted audio data to a new file

            output_filename = os.path.splitext(snippet)[0] + '.flac'
            # print(output_filename)

            # Writing the new audio of 3 mins to the desired directory
            sf.write(os.path.join("D:\\wolfesIsland\\2439985", "WolfesIsland2439985_" + output_filename),
                     snippet_data, samplerate)
