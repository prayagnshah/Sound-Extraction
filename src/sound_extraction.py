from dotenv import load_dotenv
import os
import datetime
import csv
import soundfile as sf
import numpy as np
import argparse
import logging
import sentry_sdk


# Load environment variables
load_dotenv()

# Get the sentry DSN from the environment variables
sentry_dsn = os.getenv("sentry_dsn")

sentry_sdk.init(
    dsn=sentry_dsn,
    release="v2.0.1",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
)


def main():
    def get_directories(root_directory):
        """
        Getting the directories and files from the root directory
        logging messages if no files or no extension files are found
        """
        all_files = []
        directory = []

        for root, dirs, files in os.walk(root_directory):
            ext_found = False

            for file in files:
                if file.endswith(args.extension):
                    all_files.append(file)
                    ext_found = True
                else:
                    logging.info(f"File {file} is not a {args.extension} file")

            if ext_found:
                directory.append(root)

        return directory, all_files

    def read_csv_file(csv_file_path, sampleFile, categories_col):
        """
        Reads data from a CSV file and filters it based on a column name which has sample audio files and categories column. It returns sample recordings and
        a dictionary with sample recordings as keys and categories as values.

        Args:
            csv_file_path (str): The path to the CSV file to be read.
            sampleFile (str): The name of the column containing sample audio files.
            categories_col (str): The name of the column containing categories.

        Returns:
            tuple: A tuple containing two elements:
                - list: A list of sample recordings.
                - dict: A dictionary with sample recordings as keys and categories as values.

        Steps:
            1. Open the CSV file and read its content.
            2. Find the indices of the sampleFile and categories_col columns.
            3. Extract the relevant data from the CSV file.
            4. Create a dictionary with sample recordings as keys and categories as values.
        """
        with open(csv_file_path, "r") as files:
            csv_reader = csv.reader(files)

            header = next(csv_reader)

            sampleFile_index = header.index(sampleFile)

            categories_bool = False
            if categories_col not in header:
                logging.info(
                    "Categories column not found in CSV file, so there is no folder named Nocturnal, Daytime, etc."
                )

                categories_bool = True

            else:
                categories_index = header.index(categories_col)

            rows = list(csv_reader)

        sample_recordings = [row[sampleFile_index] for row in rows]

        if categories_bool:
            categories = ["" for row in rows]

        else:
            categories = [row[categories_index] for row in rows]

        categories_dict = {k: v for k, v in zip(sample_recordings, categories)}

        return sample_recordings, categories_dict

    def process_recordings(all_files, sample_recordings):
        """
            Processes long recordings and matches them with the corresponding sample
            recordings based on their timestamps. Returns a dictionary with long
            recordings as keys and lists of associated sample recordings as values.

        Args:
            all_files (list): A list of all long recordings files.
            sample_recordings (list): A list of sample recordings files.

        Returns:
            dict: A dictionary with long recordings as keys and lists of associated
                    sample recordings as values.

        Steps:
            1. Filter and sort long recordings.
            2. Iterate through long recordings and create a dictionary to store the
                associated sample recordings.
            3. Check if a sample recording falls within a long recording's time frame.
            4. Filter the dictionary to remove empty lists and format the keys.
        """

        long_recordings = [file for file in all_files if "T" in file]

        long_recordings.sort()
        recordings_dict = {}

        for long_recording in long_recordings:
            filename, extension = os.path.splitext(long_recording)

            # Putting try and except handling because there will be backup file with .flac and we need to avoid it

            long_start_datetime = datetime.datetime.strptime(filename, "%Y%m%dT%H%M%S")

            try:
                next_long_recording = long_recordings[
                    long_recordings.index(long_recording) + 1
                ]
                next_filename, next_extension = os.path.splitext(next_long_recording)

                duration = (
                    datetime.datetime.strptime(next_filename, "%Y%m%dT%H%M%S")
                    - long_start_datetime
                )

            except IndexError:
                duration = datetime.timedelta(hours=3)

            long_end_datetime = long_start_datetime + duration

            # Create an empty list to hold sample recordings that fall within this long recording's time frame

            recordings_dict[long_start_datetime] = []

            for sample_recording in sample_recordings:
                file, ext = os.path.splitext(sample_recording)

                sample_datetime = datetime.datetime.strptime(file, "%Y%m%d_%H%M%S")

                if long_start_datetime <= sample_datetime <= long_end_datetime:
                    recordings_dict[long_start_datetime].append(sample_recording)

        # Storing the user input for the extension

        extension = args.extension

        # Removing the empty lists and showing the output with the data which has files in it

        filtered_recordings_dict = {
            key.strftime("%Y%m%dT%H%M%S") + extension: value
            for key, value in recordings_dict.items()
            if value
        }

        return filtered_recordings_dict

    def generate_subdir_name():
        """
        Function to generate a subdirectory name for the output files.
        For slice mode, the subdirectory name will be the timestamp and slice number.
        """
        user_input = input("Enter the subdirectory name: ")

        return f"{user_input}"

    def extract_audio_segments(
        filtered_recordings_dict, output_directory, site_name, categories_dict
    ):
        """
        This function extracts audio segments from a dictionary of filtered recordings
        and saves them into a specified output directory. If flag -span is used

        Args:
            filtered_recordings_dict (dict): A dictionary of filtered audio recordings.
            output_directory (str): The directory path where extracted segments will be saved.
            site_name (str): The name of the site where the recordings were taken.
            categories_dict (dict): A dictionary containing the categories of recordings.

        Steps:
            1. Generate the subdirectory name for the output directory.
            2. Create the output subdirectory.
            3. Set the duration of the audio segments to be extracted.
            4. Get the directories and files within the root directory.
            5. Loop through each directory and extract the audio segments.
        """

        subdir_name = generate_subdir_name()

        output_subdirectory = os.path.join(output_directory, subdir_name)
        os.makedirs(output_subdirectory, exist_ok=True)

        duration = datetime.timedelta(seconds=args.duration)

        directories, all_files = get_directories(root_directory)

        for directory in directories:
            recording_keys = sorted(os.listdir(directory))

            for key, value in filtered_recordings_dict.items():
                if key not in recording_keys:
                    continue

                # Trying to put in the exception handler if corrupted audio file comes up then it prints in the console and it will still continue the code instead of breaking up

                try:
                    # Loading the original audio recording file while samplefile produces array and samplerate together

                    audio_file, samplerate = sf.read(os.path.join(directory, key))

                except Exception as e:
                    logging.error(f"Error reading audio file {key}: {e}")
                    continue

                split_key = os.path.splitext(key)[0]

                start_time_parent = datetime.datetime.strptime(
                    split_key, "%Y%m%dT%H%M%S"
                )

                for snippet in value:
                    start_time_str = os.path.splitext(snippet)[0]

                    start_time = datetime.datetime.strptime(
                        start_time_str, "%Y%m%d_%H%M%S"
                    )

                    snippet_start_time = start_time - start_time_parent

                    start_frame = int(snippet_start_time.total_seconds() * samplerate)
                    end_frame = int(
                        (snippet_start_time + duration).total_seconds() * samplerate
                    )

                    current_key_index = recording_keys.index(key)

                    # Due to the fact that the audio files are not of 3 mins duration so we need to check if the duration is less than 3 mins then we need to add the next audio file to it

                    if current_key_index + 1 < len(recording_keys):
                        duration_new = datetime.timedelta(seconds=args.duration)

                        next_key = recording_keys[current_key_index + 1]

                        # Adding error handling for the next key if it is corrupted

                        try:
                            next_key_start_time = datetime.datetime.strptime(
                                os.path.splitext(next_key)[0], "%Y%m%dT%H%M%S"
                            )
                        except ValueError:
                            logging.error(
                                f"Error parsing next key {next_key} for snippet {snippet}"
                            )
                            continue

                        # Checking if the duration of the snippet is greater than the next key's start time and flag "-span" is used then it won't concatenate the audio files

                        if (
                            not args.span
                            and start_time + duration_new > next_key_start_time
                        ):
                            parent_duration_time = len(audio_file) / samplerate
                            time_duration_second = (
                                parent_duration_time
                                - snippet_start_time.total_seconds()
                            )
                            time_duration = datetime.timedelta(
                                seconds=time_duration_second
                            )

                            next_audio_file, next_samplerate = sf.read(
                                os.path.join(directory, next_key)
                            )

                            remaining_duration = duration_new - time_duration

                            remaining_audio = next_audio_file[
                                : int(
                                    remaining_duration.total_seconds() * next_samplerate
                                )
                                + 1
                            ]

                            snippet_data = np.concatenate(
                                (audio_file[start_frame:], remaining_audio)
                            )

                        else:
                            snippet_data = audio_file[start_frame:end_frame]

                    else:
                        # Extract the portion of the audio data using numpy array indexing because soundfile data comes in integers

                        snippet_data = audio_file[start_frame:end_frame]

                    extension = args.extension

                    output_filename = os.path.splitext(snippet)[0] + extension

                    # Creating the subdirectory for the categories

                    os.makedirs(
                        os.path.join(output_subdirectory, categories_dict[snippet]),
                        exist_ok=True,
                    )

                    export_segment = sf.write(
                        os.path.join(
                            output_subdirectory,
                            categories_dict[snippet],
                            site_name + output_filename,
                        ),
                        snippet_data,
                        samplerate,
                    )

        return export_segment, output_subdirectory

    def process_audio_files(directory, slice_duration, output_directory):
        """
            This function processes audio files in the given directory by slicing them
            into smaller segments of a specified duration of seconds set by user and saves them into a specified
            output directory.

        Args:
            directory (str): The directory containing the audio files to be processed.
            slice_duration (float): The duration of each sliced segment in seconds.
            output_directory (str): The directory path where sliced segments will be saved.

        Steps:
            1. Generate the subdirectory name for the output directory.
            2. Create the output subdirectory.
            3. Traverse the directory and process each audio file.
        """

        subdir_name = generate_subdir_name()

        output_subdirectory = os.path.join(output_directory, subdir_name)
        os.makedirs(output_subdirectory, exist_ok=True)

        for root, dirs, files in os.walk(directory):
            for file in files:
                file_str = os.path.splitext(file)[0]

                try:
                    file_datetime = datetime.datetime.strptime(
                        file_str, "%Y%m%dT%H%M%S"
                    )

                except ValueError:
                    logging.error(
                        f"File {file} is not in the correct format. Skipping..."
                    )
                    continue

                try:
                    audio, sample_rate = sf.read(os.path.join(root, file))
                except Exception as e:
                    logging.error(f"Error in the audio file {file}: {e}")
                    continue

                total_samples = len(audio)

                chunk_samples = int(slice_duration * sample_rate)

                start = 0

                for i in range(0, total_samples, chunk_samples):
                    chunk = audio[i : i + chunk_samples]

                    recording_time = (
                        file_datetime + datetime.timedelta(seconds=start)
                    ).strftime("%Y%m%dT%H%M%S")

                    filename = os.path.join(
                        output_subdirectory,
                        "{}{}".format(recording_time, args.extension),
                    )

                    sf.write(filename, chunk, sample_rate)

                    start += slice_duration

    # fmt: off
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(
        description='A program that will help to extract recording from the actual long recordings.')

    parser.add_argument('-r', '--root_directory', type=str, required=True, help='The path to the folder containing the original recordings')  
    parser.add_argument('-o', '--output_directory', type=str, help='The path to the folder of the extracted audio segments')  
    parser.add_argument('-c', '--csv_file_path', type=str, help='The path to the CSV file. The header must include "sampleFile" and may include a "category" column. Recording named within the "sampleFile" column should be in the format "YYYYMMDD_HHMMSS"; if included, subgroups within "category" can be defined by the user, the recordings_times_generator.py (https://github.com/prayagnshah/Sound-Extraction/blob/main/src/README.md), or left blank"') 
    parser.add_argument('-d', '--duration', type=float, default=180, help='The desired duration of the extracted segments')  
    parser.add_argument('-s', '--site_name', type=str,  help='The name of the site')
    parser.add_argument('-span', '--span', action='store_true', help='Extract original files instead of spanning; see README for more information') 
    parser.add_argument('-e', '--extension', type=str, choices=['.wav', '.flac'], default='.flac', help='The extension of the original audio files')
    parser.add_argument('-slice', '--slice', type=float, help='Duration (in seconds) of the sliced audio files') 
    # Parse the command line arguments

    args = parser.parse_args()

    # fmt: on

    # Getting the root directory and output directory from the user

    root_directory = args.root_directory
    output_directory = args.output_directory
    site_name = args.site_name
    csv_file_path = args.csv_file_path

    # Create the log file name using the output directory

    log_file = os.path.join(output_directory, "sound_extraction_logs.txt")
    log_format = "%(asctime)s - %(levelname)s - %(message)s"

    # Creating the log format

    logging.basicConfig(format=log_format, level=logging.INFO, filename=log_file)

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
        categories_col = "category"
        sample_recordings, categories_dict = read_csv_file(
            csv_file_path, sampleFile, categories_col
        )

        filtered_recordings_dict = process_recordings(all_files, sample_recordings)

        export_segment, output_directory = extract_audio_segments(
            filtered_recordings_dict, output_directory, site_name, categories_dict
        )


if __name__ == "__main__":
    main()
