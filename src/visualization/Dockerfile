# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (if any)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install jupyter
RUN mkdir -p /app/results
COPY scripts/visualization.ipynb /app/visualization.ipynb
EXPOSE 8888
RUN pip install nbconvert
# Add /app to PYTHONPATH
ENV PYTHONPATH="/app:${PYTHONPATH}"
CMD ["sh", "-c", "jupyter nbconvert --to notebook --execute /app/visualization.ipynb --output /app/visualization_executed.ipynb && jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --NotebookApp.token='' --NotebookApp.open_browser=False --allow-root /app/visualization_executed.ipynb"]