# Audio-File Extraction

## About

This is the tool to extract bird sounds from the long audios and slice the BAT recordings into smaller parts to make it compatible with the analysis workflow. Moreover, software like SonoBAT will be able to handle the recordings.

Get your extracted audio files new dimension according to the sunrise, sunset, nocturnal, dusk, etc.

Extraction will work for both type of format of files (wav and flac).

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

1.  Run sound_extraction.py to get the extracted audio files. You need to set the path where the downloaded files are there. Here is an example:

    python sound_extraction.py -r "/path/to/original/audio/files" -o "/path/to/output/folder" -c "/path/to/csv/file" -s "site_name"

Arguments and commands used are required to get the extraction of audio files according to the sample times.

2.  Run sound_extraction.py to get the sliced audio files which can handle around 192K sample rate. Here is an example:

    python sound_extraction.py -r "/path/to/original/audio/files" -o "/path/to/output/folder" -slice 10

Arguments and commands used are required to get the slicing of larger audio files into smaller audio files of your choice.

Here's a complete list of all command line arguments:

    -r, Path to original audio files (required). Need to make sure all the audio are stored in the folder.
    -o, Path to output folder (required). Need to make sure all the folder is created.
    -c, Path to csv file (required). CSV file where all the sample recordings names are stored and sample recording should have the column name "sampleFile".
    -s, Site name (required). Name of the site.
    -d, Duration of the extracted audio file  (optional). You can change the duration and can have whatever choice of extracted recordings. Default is 3 minutes.
    -span, Span of the audio file (optional). Extracted audio files will not span to 3 minutes if the original file is shorter.
    -e, Extension of the audio file (optional)(.wav or .flac). If your original audio files are flac then you need to use ".wav". Default is flac.
    -slice, Slice the audio file (optional). If you want to slice the larger audio file into smaller audio files then you can use this argument.

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

1. If your recorders are taking time in creating a log file for every recording then spanning of files can give off times. For eg, if recorder is 1 hour long but and it takes 6 seconds to create a log file then original length of audio file will be 59 minutes and 54 seconds. If the sample file falls near the end of the original recording then extraction of audio might be 2 mins 54 seconds. In this scenario, you need to adjust the `seconds` on `line 212` in file `sound_extraction.py`

   `duration_new = datetime.timedelta(minutes=args.duration, seconds=6)`

2. If you are using `wav` files then you will need to do the same as above.

## Future Plans

1. Make code more robust that if there are unused files in the directory then also code keeps on running and does not stop.

2. Want to make sure that if we use increment of 3 minutes then it should not span to less than 3 minutes or greater than 3 minutes.
