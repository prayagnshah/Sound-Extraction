import csv
import os


# ----------------------- Changing the file name with date T time to get the data according to the script. This script is for .wav files to rename it
# dir = ["D:\\wolfesIsland\\converted-to-wav-2439985"]

# for directory in dir:
#     new_file = os.listdir(directory)

#     for file in new_file:
#         # print(file)
#         if file.endswith(".wav"):
#             filepath = os.path.join(directory, file)
#             # print(filepath)

#             try:
#                 date_time = file.split("_")[2].split("+")[0]
#             # print(date_time)
#                 date_time = date_time[:-5]

#             except IndexError:
#                 continue

#             new_final_name = date_time + ".wav"
#             # print(new_final_name)

#             # print(new_final_name)

#             new_filepath = os.path.join(directory, new_final_name)
#             # print(new_filepath)

#             os.rename(filepath, new_filepath)


# ---------------------- This is the script to rename and it is for flac files. To rename flac files

root_directory = "D:\\HogIsland\\2019511"

for subdir, dirs, files in os.walk(root_directory):

    for file in files:
        # print(file)
        if file.endswith(".flac"):
            filepath = os.path.join(subdir, file)
            # print(filepath)

            date_time = file.split("_")
            # print(date_time)
            try:
                time = date_time[2].split("-")[0]

            except IndexError:
                continue

            # To concatenate we need to convert to str

            timestamp = time[0:15]

            new_final_name = timestamp + ".flac"

            new_filepath = os.path.join(subdir, new_final_name)

            os.rename(filepath, new_filepath)


# print(new_filepath)

# print(new_filepath)


# ----------------------- To read the particular column in csv file
# with open('C:/Users/ShahP/Downloads/OwlsHead_RecordingDrawTEST.csv', 'r') as file:

#     # Creating the csv object
#     csv_reader = csv.reader(file)

#     # Reading the header row
#     header = next(csv_reader)

#     # Fidning the index column
#     sampleFile_index = header.index('sampleFile')

#     # print(sampleFile_index)

#     for file in csv_reader:
#         sampleFile_value = file[sampleFile_index]

#     # print(sampleFile_value)


# ------------------------- This is the script where we can convert flac files to wav files and multiple flac files at once. Very cool!

# root_flac_directories = "D:\\wolfesIsland\\2439985"
# wav_directory = "D:\\wolfesIsland\\converted-to-wav-2439985"

# for subdir, dirs, files in os.walk(root_flac_directories):

#     for filename in files:
#         if filename.endswith(".flac"):

#             input_path = os.path.join(subdir, filename)
#             # print(input_path)
#             output_path = os.path.join(
#                 wav_directory, os.path.splitext(filename)[0] + '.wav')
#             print(output_path)

#             # This will run the ffmpeg program and convert the files to wav
#             os.system(
#                 f'C:\\Users\\ShahP\\Documents\\ffmpeg\\bin\\ffmpeg.exe -i "{input_path}" "{output_path}"')
