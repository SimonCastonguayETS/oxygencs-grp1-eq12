# Use an official Python runtime as a parent image
FROM python:3.6-alpine AS builder

# Set the working directory in the container to /usr/src/app
WORKDIR /usr/src/app

# Copy the entire project directory (including the src folder) into the container at /usr/src/app
COPY requirementsDocker.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirementsDocker.txt

COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

# Change the working directory to /usr/src/app/src where main.py is located
WORKDIR /usr/src/app/src

# Run main.py when the container launches
CMD ["python", "main.py"]