# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.3] - 2023-11-06

- Fixed the structure of argument start date and end date. i.e start-date to start_date and end-date to end_date.
- Updated the readme by including the research paper. 
- Program is able to accept float values in duration and slice timing. 
- Setup.py file is updated so that Python program will work with Python 3.9.0 and 3.10.0 versions. 

## [2.0.2] - 2023-08-14

### Fixed

- Fixed the issue in having extracted files with two dots in the extension. The files are being extracted in proper format now.
- Fixed the minor changes in the JOSS paper .bib and .md files.

### Added

- Added the timezones list which are supported by the program in the README.md file.

## [2.0.1] - 2023-07-20

### Fixed

- Fixed the issue of CSV file output from recording_times_generator.py file. The CSV file was not being generated in the correct format. The issue has been fixed now. The CSV file is being generated in the correct format now.

## [2.0.0] - 2023-07-19

### Added (Breaking Changes)

- Added unittests for the sound_extraction.py file and recording_times_generator.py file.
- Added code of conduct file.
- Added the files without the argparse for unittests.
- Added JOSS paper and references. 
- Added the command recording_times_generator to run the program from CLI to extract the samples names and times according to the sunlight phases.

### Changed

- Improved CLI documentation to reflect the availability of both commands and their respective usage instructions. sound_extraction.py and recording_times_generator.py.
- Changed the pypi version to 2.1.2.
- Changed the functions to sound_extraction and recording_times_generator to allow the users use from CLI. 
- Renamed the CLI command to sound_extraction for sound extraction operations. Users should now use sound_extraction instead of the previous command sound-extraction to perform sound extraction tasks. Name change has been done to remain consistent the program name.

## [1.1.2] - 2023-06-19

### Added

- Added Dockerfile for the users to run the program through docker.

### Changed

- Changed the column name in the CSV file from `Categories` to `category` as per user's request.
- Changed the argument description for CSV file in the `README.md` file.

[unreleased]:

- Need to reduce the complexity time of the program.


## [1.1.1] - 2023-06-15

### Added

- Functionality added to store the extracted recordings in the specific time folders. For instance, Nocturnal, Daytime, etc.
- Functionality added to download the package from pip and run it from the command line.

### Changed

- Changed the argument description for CSV file in the `README.md` file.

[unreleased]:

- Need to create Dockerfile

## [1.0.1] - 2023-06-12

### Added

- Added `setup.py` file
- Added `VERSION` file
- Package published on PyPI

### Changed

- Changed `README.md` file
- Initialized main() function in sound_extraction.py file

### Removed

- Removed `VERSION` file

[unreleased]:

- Need to create Dockerfile
- Need to create folders of specific time `Nocturnal, Daytime, etc` for the extracted recordings

## [1.0.0] - 2023-06-07

### Added

- Initial release
- Added `README.md` and `CHANGELOG.md` files
- Added `LICENSE` file
- Added `requirements.txt` file

[unreleased]:

- Need to publish the package on PyPI
- Need to create Dockerfile
