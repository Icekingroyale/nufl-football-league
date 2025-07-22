# Use official Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Create the uploads directory for Choreo
RUN mkdir -p /app/uploads

# Expose the port the app runs on
EXPOSE 8080

# Set environment variables
ENV FLASK_APP=app.py

# Run the app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"] 