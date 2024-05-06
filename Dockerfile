########################################################################################
# Author: Romba 
# Date: 04/05/2024
# Comment: Dockerfile to execute the full Home project.
########################################################################################

# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install requests

# Run main.py when the container launches
CMD ["python", "scripts/habyt_99_home_exercise.py"]
