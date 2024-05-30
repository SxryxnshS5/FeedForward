# Use an official Ubuntu runtime as a parent image
FROM ubuntu:20.04

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies and Python 3.7
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.7 \
    python3.7-dev \
    python3-pip \
    libxcrypt1 \
    && apt-get clean

# Install pip for Python 3.7
RUN python3.7 -m pip install --upgrade pip

# Set python3.7 as the default python
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
