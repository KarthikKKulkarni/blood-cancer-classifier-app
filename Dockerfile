FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y python3-tk libgl1-mesa-glx libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Install required Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the application
CMD ["python", "blood_cancer_classifier.py"]
