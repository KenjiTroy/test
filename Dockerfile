# Use a Python base image
FROM python:3.9-bullseye

# Install system dependencies, including Tesseract and its libraries
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && apt-get clean

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port your Flask app will run on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
