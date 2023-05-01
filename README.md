# Audio-File Extraction

## About

Use this tool to segment (i.e., clip or slice), copy, and extract short-duration recordings, from long-duration WAV or FLAC files. Segmenting audio files into smaller parts can make recordings compatible for certain analytical workflows and allow for easier manipulation and sharing. Segment and extracting recordings based on a list of recording start times (date times) and a desired duration. This allows for applications such as the extraction of stratified audio samples, among others.

## Setup (Windows)

Download Audio-File Extraction Files: [Sound-File Extraction](https://drive.google.com/file/d/1HX9Cz0I7uKsIPuhHCdB1lfCmbtFY_YxJ/view?usp=share_link)

    python -m venv venv
    venv\Scripts\Activate
    pip install -r requirements.txt

If creating virtual environment gives us an error then open the Powershell with <b>administrator</b> and run the following command:

    Set-ExecutionPolicy Unrestricted

## Setup (Linux)

Download Audio-File Extraction Files: [Sound-File Extraction](https://drive.google.com/file/d/1HX9Cz0I7uKsIPuhHCdB1lfCmbtFY_YxJ/view?usp=share_link)

    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

## Test Files Usage

Download Test Files: [Test Files](https://drive.google.com/file/d/1iBrAkaLagScc3kRuLkFw_2eUovGU2d8L/view?usp=share_link)

    python sound_extraction.py -r "/path/to/original/audio/files" -o "/path/to/output/folder" -c "/path/to/csv/file" -s "site_name"

## Usage

1.  Run sound_extraction.py to get the extracted audio files. You need to set the working directory where the downloaded files are located. Here is an example:

    python sound_extraction.py -r "/path/to/original/audio/files" -o "/path/to/output/folder" -c "/path/to/csv/file" -s "site_name"

Arguments and commands used are required to get the extraction of audio files according to the sample times.

2.  Run sound_extraction.py to get the sliced audio files which can handle around 192K sample rate. Here is an example:

    python sound_extraction.py -r "/path/to/original/audio/files" -o "/path/to/output/folder" -slice 10

Arguments and commands used are required to get the slicing of larger audio files into smaller audio files of your choice.

Here's a complete list of all command line arguments:

    -r, Path to original audio files (required). Need to make sure all the audio files are stored in a folder.
    -o, Path to output folder (required). Make sure to create this folder before running the command.
    -c, Path to your list of recordings to be extracted. This must be a CSV file where all the sample recording names to be extracted, stored in a column named "sampleFile".
    -s, Prefix or the recording name, or ID, etc. This will be used to name the extracted audio files.
    -d, Duration of the extracted audio file. Change the duration of the extracted audio files, if required. Default is 3 minutes.
    -span, Span of the audio file. Extracted audio files will not span to 3 minutes if the original file is shorter.
    -e, Extension of the audio file (.wav or .flac). If your original audio files are flac then you need to use ".wav". Default is flac.
    -slice, Slice the audio file in smaller segments/chunks. Default is 10 seconds.

We can see the arguments list by using the following command:

    python sound_extraction.py -h

2. This is very basic version of the analysis of the workflow, you can adjust it to your needs.

3. Please open an issue if you have any questions or suggestions to add any features.

4. I will keep on updating the code and making it more efficient.

## Important Notes

1. Original audio files should be in subfolder of root directory and once you provide path of root folder then code will search for all the files in all subfolders.

2. Original files should be in the format `20220611T202300.wav` or `20220611T202300.flac`. Sample files in CSV should be in the format `20220611_202300.wav` or `20220611_202300.flac`.

3. Need to make sure directories do not have any other files except the original audio files.

## Issues

1. If your recorders are taking time in creating a log file for every recording then spanning of files can give off times. For eg, if recorder is 1 hour long but it takes 6 seconds to create a log file then original length of audio file will be 59 minutes and 54 seconds. Furthermore, if the sample file falls near the end of the original recording then extraction of audio might be 2 mins 54 seconds. In this scenario, you need to adjust the `seconds` on `line 213` or `line 215` depending on the type of audio and this changes should be made in file `sound_extraction.py`.

   ```
   if args.extension == ".flac":
       seconds = 6
   elif args.extension == ".wav":
       seconds = 1
   ```

2. If you are using `wav` files then you will need to do the same as above.

## Future Plans

1. Make code more robust that if there are unused files in the directory then also code keeps on running and does not stop.

2. Want to make sure that if we use increment of 3 minutes then it should give us exactly 3 minutes of audio file instead of adding 6 seconds or 1 seconds in the code.
