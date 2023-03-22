import datetime
import os
import csv
from pydub import AudioSegment


# Getting all the files in the directory

directory = "D:/owlsHead/rawData/SD3_20220614/20210701"
all_files = os.listdir(directory)


with open('C:/Users/ShahP/Downloads/OwlsHead_RecordingDrawTEST.csv', 'r') as files:

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


# Filtering in actual recordings

long_recordings = [file for file in all_files if "T" in file]

recordings_dict = {}

for long_recording in long_recordings:

    # Splitting the .wav extension from the filename so datetime can be parsed

    filename, extension = os.path.splitext(long_recording)

    # Get the start and end datetime of the long recording

    long_start_datetime = datetime.datetime.strptime(
        filename, "%Y%m%dT%H%M%S")

    # Getting the duration of the recording by checking the next long recording's start time and if there is one then,

    try:
        next_long_recording = long_recordings[long_recordings.index(
            long_recording) + 1]
        next_filename, next_extension = os.path.splitext(next_long_recording)
        duration = datetime.datetime.strptime(
            next_filename, "%Y%m%dT%H%M%S") - long_start_datetime

    # Assuming the last recording of 3 hours

    except IndexError:

        duration = datetime.timedelta(hours=3)

    long_end_datetime = long_start_datetime + duration

    # Create an empty list to hold sample recordings that fall within this long recording's time frame
    # Using if condition to check that sample recording falls into long recording
    # Finally producing the output: sample_recording

    recordings_dict[long_start_datetime] = [
        sample_recording for sample_recording in sample_recordings
        if long_start_datetime <= datetime.datetime.strptime(
            os.path.splitext(sample_recording)[0], "%Y%m%d_%H%M%S") <= long_end_datetime
    ]


# Removing the empty lists and showing the output with the data which has files in it

filtered_recordings_dict = {
    key.strftime("%Y%m%dT%H%M%S") + ".wav": value for key, value in recordings_dict.items() if value
}

# print(filtered_recordings_dict)

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

        # Converting into milliseconds as Audio segment accepts only ms

        snippet_start_time_ms = (
            snippet_start_time).total_seconds() * 1000

        # 3 minutes increment for extracted audio and converting to milliseconds as AudioSegment only accepts that
        end_time = start_time + datetime.timedelta(minutes=3)

        # Trying to get the snippet's end time from actual recording

        snippet_end_time = snippet_start_time + datetime.timedelta(minutes=3)
        snippet_end_time_ms = snippet_end_time.total_seconds() * 1000

        # Extracting the 3 minute audio file using start and end time in milliseconds as Audiosegment only wants that

        three_minute_audio = audio_file[snippet_start_time_ms:snippet_end_time_ms]

        output = three_minute_audio.export(
            f"{start_time_str}.wav", format="wav")
