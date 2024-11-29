# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Set the environment variable to avoid buffering of logs
ENV PYTHONUNBUFFERED=1

# Run the Flask app when the container starts
CMD ["python", "main.py"]
