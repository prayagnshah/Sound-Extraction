# Base Image
FROM python:3.8-slim-buster

# Copying all the contents to the app folder
COPY . /app

# Setting up the working directory
WORKDIR /app

# Installing all the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Usage commands
ENTRYPOINT [ "python", "src/sound_extraction.py" ]