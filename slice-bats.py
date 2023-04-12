import os
from datetime import timedelta, datetime
import soundfile as sf


# What increment value to use for the chunks

chunk_duration = 10

# Path to the directory containing the audio files

directory = "C:\\Users\\ShahP\\Documents\\extract-audio-files\\audio"

# Get all the files in the directory

list_files = os.listdir(directory)

# Loop through the files

for file in list_files:
    file_str = os.path.splitext(file)[0]
    file_datetime = datetime.datetime.strptime(file_str, "%Y%m%dT%H%M%S")

    audio, sample_rate = sf.read(os.path.join(directory, file))

    # total samples in the audio file

    total_samples = len(audio)

    # samples in each chunk

    chunk_samples = int(chunk_duration * sample_rate)

    start = 0

    for i in range(0, total_samples, chunk_samples):

        chunk = audio[i:i + chunk_samples]

        # Getting the start time of the audio file from the actual recordings and adding the chunk duration
        recording_time = (
            file_datetime + datetime.timedelta(seconds=start)).strftime("%Y%m%dT%H%M%S")

        filename = "C:\\Users\\ShahP\\Documents\\extract-audio-files\\extract\\{}.wav".format(recording_time)  # nopep8

        sf.write(filename, chunk, sample_rate)

        start += chunk_duration
