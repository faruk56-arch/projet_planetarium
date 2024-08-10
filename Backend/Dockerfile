# Use a base image with Python 3.9
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install necessary OS packages
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev  # This will install Python development headers

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Command to run on container start
CMD ["python3", "app.py"]
