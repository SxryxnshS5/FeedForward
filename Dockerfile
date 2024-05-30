# Use an official Python runtime as a parent image
FROM python:3.12-slim-buster

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libcrypt1 \
    libxcrypt1 \
    libpython3.7 \
    && apt-get clean

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
