import os
import datetime
import soundfile as sf


def process_audio_files(directory, chunk_duration, output_directory):

    # Get all the files in the directory

    list_files = os.listdir(directory)

    # Loop through the files
    for file in list_files:
        file_str = os.path.splitext(file)[0]
        file_datetime = datetime.datetime.strptime(file_str, "%Y%m%d_%H%M%S")

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

            filename = os.path.join(
                output_directory, "{}.wav".format(recording_time))

            sf.write(filename, chunk, sample_rate)

            start += chunk_duration


directory = "D:\\bats\\countryIsland\\SD1\\Data1"
output_directory = "C:\\Users\\ShahP\\Documents\\extract-audio-files\\extract"
chunk_duration = 10

process_audio_files(directory, chunk_duration, output_directory)
