from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sound-extraction",
    version="2.0.4",
    packages=["src"],
    install_requires=[
        "certifi>=2023.5.7",
        "cffi>=1.15.1",
        "load-dotenv>=0.1.0",
        "numpy>=1.24.3",
        "pycparser>=2.21",
        "python-dotenv>=1.0.0",
        "sentry-sdk>=1.25.1",
        "soundfile>=0.12.1",
        "urllib3>=2.0.3",
        "astral>=3.2",
        "backports.zoneinfo==0.2.1; python_version<'3.9'",
        "pytz>=2023.3",
        "tzdata>=2023.3",
    ],
    entry_points={
        "console_scripts": [
            "sound_extraction = src.sound_extraction:main",
            "recording_times_generator = src.recording_times_generator:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Prayag Shah",
    author_email="prayagshah07@gmail.com",
    url="https://github.com/prayagnshah/Sound-Extraction",
)
