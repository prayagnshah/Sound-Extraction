import datetime
import os
from pydub import AudioSegment

# Getting all the files in the directory

directory = "C:\\Users\\ShahP\\OneDrive - EC-EC\\owlhead-testing-recordings"
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
    long_end_datetime = long_start_datetime + \
        datetime.timedelta(hours=2, minutes=59, seconds=59)

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

# print(recordings_dict)

dir = "C:\\Users\\ShahP\\OneDrive - EC-EC\\owlhead-testing-recordings"

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

    # Loop through each specified snippet in the value
    for snippet in value:
        start_time_str = os.path.splitext(snippet)[0]

        # Extract the start and end time for the snippet and parsing string as datetime object
        start_time = datetime.datetime.strptime(
            start_time_str.split("_")[1], "%H%M%S")

        # 3 minutes increment for extracting audio and converting to milliseconds as AudioSegment only accepts that
        end_time = start_time + datetime.timedelta(milliseconds=180000)

        # Extracting the audio snippet
        # audio_snippet = audio_file[start_time:end_time]
        # print(audio_snippet)
        # audio_snippet.export(os.path.join(directory, snippet), format="wav")
