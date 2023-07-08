# Use the official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app files into the container
COPY . .

# Expose the port on which the app will run
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=EldarNumerology.py

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
