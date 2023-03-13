import datetime
import os

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

print(recordings_dict)

# Converting into dictionary format to print key and value differently

# for key, value in recordings_dict.items():
#     key_str = key.strftime("%Y%m%d_%H%M%S")

#     key_str = key_str + ".wav"

#     values_str = [str(val) for val in value]
#     print(key_str, values_str)
