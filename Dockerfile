#Use the official Python image with a specific version
FROM python:3.9-slim

# Set environment variables to avoid buffer issues and prevent writing .pyc files
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install system dependencies, including Tesseract-OCR
RUN apt-get update && apt-get install -y \
    libgl1 \
    tesseract-ocr \
    libtesseract-dev \
    gcc \
    g++ \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN  python -m pip install --upgrade pip && \
     pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY src /app/

# Expose the port Flask will run on
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
