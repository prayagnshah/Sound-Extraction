import datetime
import os
from pydub import AudioSegment

# Getting all the files in the directory

directory = "C:/Users/ShahP/Documents/extract-audio-files-wav"
all_files = os.listdir(directory)


# Filtering the sample recordings

sample_recordings = [file for file in all_files if "_" in file]

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
    recordings_dict[long_start_datetime] = []

    for sample_recording in sample_recordings:

        file, ext = os.path.splitext(sample_recording)

        # Get the datetime of the sample recording
        sample_datetime = datetime.datetime.strptime(
            file, "%Y%m%d_%H%M%S")

        # Check if the sample recording falls within the current long recording's time frame
        if long_start_datetime <= sample_datetime <= long_end_datetime:
            recordings_dict[long_start_datetime].append(sample_recording)


# Filtering key value pairs which has the values in it

filtered_recordings_dict = {}
for key, value in recordings_dict.items():
    if value:
        key_str = key.strftime("%Y%m%dT%H%M%S") + ".wav"
        filtered_recordings_dict[key_str] = value

# print(filtered_recordings_dict)

# Looping through each key-value pair

for key, value in filtered_recordings_dict.items():

    # Loading the 3-hour audio recording file
    audio_file = AudioSegment.from_wav(os.path.join(directory, key))

    # Splitting the key values into datetime

    split = os.path.splitext(key)[0]

    # Loop through each specified snippet in the value

    for snippet in value:
        start_time_str = os.path.splitext(snippet)[0]
        # print(start_time_str)

        # Extract the start and end time for the snippet and parsing string as datetime object

        start_time = datetime.datetime.strptime(
            start_time_str, "%Y%m%d_%H%M%S")

        # Getting the start time of the audio file from the actual recordings

        start_time_parent = datetime.datetime.strptime(
            split, "%Y%m%dT%H%M%S")

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
