# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
