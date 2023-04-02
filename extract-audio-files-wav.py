import datetime
import os
import csv
from pydub import AudioSegment


# Getting all the files in the directory
# Trying to establish that we can use multiple directories at once

root_directory = "C:\\Users\\ShahP\\Music"

# Using os.walk so that it can traverses to all the directories

for root, dirs, files in os.walk(root_directory):

    # Looping the files of that directory. Dirs will take all the inside directories

    for directory_path in dirs:

        directory = os.path.join(root, directory_path)

        # Setting up the exception handler if directory path is wrong still the code will keep moving
        # In console we will be able to get to know which directory was corrupt
        try:
            all_files = os.listdir(directory)
            # print(all_files)
        except FileNotFoundError as e:
            print(
                f"Directory path {directory} not found. Skipping this directory...")
            continue

        # print(all_files)

        with open('C:\\Users\\ShahP\\Downloads\\bossSample-data.csv', 'r') as files:

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

            long_start_datetime = datetime.datetime.strptime(
                filename, "%Y%m%dT%H%M%S")

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

            recordings_dict[long_start_datetime] = []

            # Create an empty list to hold sample recordings that fall within this long recording's time frame
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
        # print(recordings_dict)

        # recordings_dict[long_start_datetime] = [
        #     sample_recording for sample_recording in sample_recordings
        #     if long_start_datetime <= datetime.datetime.strptime(
        #         os.path.splitext(sample_recording)[0], "%Y%m%d_%H%M%S") <= long_end_datetime
        # ]

        # Removing the empty lists and showing the output with the data which has files in it

        filtered_recordings_dict = {
            key.strftime("%Y%m%dT%H%M%S") + ".wav": value for key, value in recordings_dict.items() if value
        }

        # print(filtered_recordings_dict)

        recording_keys = sorted(os.listdir(directory))
        # print(recording_keys)

    # Looping through each key-value pair

        for key, value in filtered_recordings_dict.items():

            # Loading the 3-hour audio recording file
            audio_file = AudioSegment.from_wav(os.path.join(directory, key))

            # Splitting the key values into datetime

            split_key = os.path.splitext(key)[0]

            # Loop through each specified snippet in the value

            for snippet in value:
                start_time_str = os.path.splitext(snippet)[0]
                # print(start_time_str)

                # Extract the start and end time for the snippet and parsing string as datetime object

                start_time = datetime.datetime.strptime(
                    start_time_str, "%Y%m%d_%H%M%S")

                # Getting the start time of the audio file from the actual recordings

                start_time_parent = datetime.datetime.strptime(
                    split_key, "%Y%m%dT%H%M%S")

                # Getting the actual start time of the snippet in the audio file

                snippet_start_time = start_time - start_time_parent
                # print(snippet_start_time)

                # Converting into milliseconds as Audio segment accepts only ms

                snippet_start_time_ms = (
                    snippet_start_time).total_seconds() * 1000
                # print(type(snippet_start_time_ms))

                # Trying to get the snippet's end time from actual recording

                snippet_end_time = snippet_start_time + datetime.timedelta(minutes=3)  # nopep8

                # Calculate the end time of the current recording file

                end_time_parent = datetime.datetime.strptime(os.path.splitext(
                    filtered_recordings_dict[key][-1])[0], "%Y%m%d_%H%M%S")

                # Converting the end time of the snippet into milliseconds

                snippet_end_time_ms = snippet_end_time.total_seconds() * 1000

                # Extracting the index of the current key from the list of original recording keys

                current_key_index = recording_keys.index(key)

                if current_key_index + 1 < len(recording_keys):

                    # Find the next key from the list of original recording keys

                    next_key = recording_keys[current_key_index + 1]

                    # Splitting the original recording without the extension

                    next_split_key = os.path.splitext(next_key)[0]

                    # Converting the parent recording's end time into datetime object

                    end_time_parent = datetime.datetime.strptime(
                        next_split_key, "%Y%m%dT%H%M%S")

                    # Check if the snippet time is beyond the end of current recording file

                    # print(snippet_end_time, end_time_parent, start_time_parent)
                    # Checking the snippet end time is greater than the end time of the parent recording

                    if snippet_end_time > end_time_parent - start_time_parent:

                        next_audio_file = AudioSegment.from_wav(os.path.join(directory, next_key))  # nopep8

                        # Calculate the remaining time of the snippet

                        remaining_time = snippet_end_time - (end_time_parent - start_time_parent)  # nopep8

                        # Converting the remaining time into milliseconds

                        remaining_time_ms = remaining_time.total_seconds() * 1000

                        # Extracting the remaining audio from the next recording

                        remaining_audio = next_audio_file[:int(
                            remaining_time_ms)]

                        # Concatenate the remaining audio with the current 3-minute snippet
                        three_minute_audio = audio_file[snippet_start_time_ms:] + remaining_audio  # nopep8

                    else:

                        # Extracting the 3 minute audio file using start and end time in milliseconds as Audiosegment only wants that

                        three_minute_audio = audio_file[snippet_start_time_ms:snippet_end_time_ms]  # nopep8

                else:

                    # Extracting the 3 minute audio file using start and end time in milliseconds as Audiosegment only wants that

                    three_minute_audio = audio_file[snippet_start_time_ms:snippet_end_time_ms]

                # User can just change the directory name and then can save the output files. Format is already been provided

                output = three_minute_audio.export(
                    "C:\\Users\\ShahP\\Music\\HogIsland_{}.wav".format(start_time_str), format="wav")
