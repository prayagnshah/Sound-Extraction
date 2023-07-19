# Recording Times Generator (CSV file)

## Installation 

1. Download the python package:
    
    `pip install sound-extraction`

    a. After the installation you can use the following command to run the program or use `--help` to see the arguments list:

    `recording-times-generator --latitude 32.6574 --longitude -85.4443 --start-date 2021-01-01 --end-date 2021-01-07 --timezone "Canada/Atlantic"`


## Arguments

Here's a complete list of arguments that can be used with the program:

    -h, --help            show this help message and exit
    -lat LATITUDE, --latitude LATITUDE
                            Latitude of the site
    -lon LONGITUDE, --longitude LONGITUDE
                            Longitude of the site
    -start START_DATE, --start_date START_DATE
                            Start date of the sampling period
    -end END_DATE, --end_date END_DATE
                            End date of the sampling period
    -t TIMEZONE, --timezone TIMEZONE
                            Timezone of the site you want to sample
    -sample SAMPLE_SIZE, --sample_size SAMPLE_SIZE
                            Number of samples per category
    -s SITE_NAME, --site_name SITE_NAME
                            The name of the site
    -ext EXTENSION, --extension EXTENSION
                            The extension of the original audio files
    -o OUTPUT, --output OUTPUT
                            The path to the folder of the extracted sample audio files

If a user provides a directory as the output path, the program will create a folder with the `samples.csv` file. If the file name is mentioned along with the directory, then it will create the file with the given name. If the output argument is not specified, the `samples.csv` file will be created in the current directory.

This will generate a CSV file with random sampling times for the given location and dates and then this sampling can be used to extract the audio files from the original recordings. After this you can follow the instructions at this [file](https://github.com/prayagnshah/Sound-Extraction/blob/main/README.md)