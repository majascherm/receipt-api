# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /receipt-api

# Copy the current directory contents into the container
COPY . /receipt-api

# Install any necessary dependencies (if you have a requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Run the Python script when the container starts
CMD ["python", "processor.py"]
