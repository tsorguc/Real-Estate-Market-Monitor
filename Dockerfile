# Use python:3.12-slim base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Install system dependencies if required for compiling certain python libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt to install dependencies
COPY requirements.txt .

# Clean requirements.txt by removing Windows-only libs (like pywinpty) to avoid Linux installation errors
RUN sed -i '/pywinpty/d' requirements.txt

# Filter out heavy ML/multimedia dependencies to keep the image lean and speed up build
RUN grep -E -i 'dash|pymongo|gunicorn|websockets|pandas|numpy|plotly|dotenv|pillow|tqdm|requests|jinja2|werkzeug|flask' requirements.txt > req_dash.txt

# Install python dependencies
RUN pip install --no-cache-dir -r req_dash.txt

# Copy project files into the container
COPY . .

# Expose port 8050 for the Dash application
EXPOSE 8050

# Set default host/port environment variables
ENV HOST=0.0.0.0
ENV PORT=8050

# Run using Gunicorn production WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:8050", "--workers", "2", "app:server"]
