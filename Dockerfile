# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Make the entrypoint executable
RUN chmod +x entrypoint.sh

# Run the app
ENTRYPOINT ["./entrypoint.sh"]
