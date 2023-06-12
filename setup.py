from setuptools import setup, find_packages

setup(
    name='sound-extraction',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'certifi==2023.5.7',
        'cffi==1.15.1',
        'load-dotenv==0.1.0',
        'numpy==1.24.3',
        'pycparser==2.21',
        'python-dotenv==1.0.0',
        'sentry-sdk==1.25.1',
        'soundfile==0.12.1',
        'urllib3==2.0.3',
    ],
    entry_points={
        'console_scripts': [
            'sound-extraction = sound_extraction:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={'': 'sound-extraction'},
    description="Slice and segment your audio files easily with open source Python program. Our tool enables you to perform analytical workflows by creating segments based on recording start time and desired duration. Share and manipulate the recordings at ease.Slice and segment your audio files easily with open source Python program. Our tool enables you to perform analytical workflows by creating segments based on recording start time and desired duration. Share and manipulate the recordings at ease.",
    author="Prayag Shah",
    author_email="prayagshah07@gmail.com",
    url="https://github.com/prayagnshah/Sound-Extraction",

)
