# Use an official Python runtime as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports for Streamlit and FastAPI
EXPOSE 8000
EXPOSE 8501

# Run both Streamlit and FastAPI via a Python runner
CMD ["python", "app/app.py"]