# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install Tesseract and necessary dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

# Copy the application code
COPY . /app/
WORKDIR /app

# Expose the port the app will run on
EXPOSE 5000

# Set the environment variable for Tesseract
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/

# Run the Flask app
CMD ["python", "app.py"]
