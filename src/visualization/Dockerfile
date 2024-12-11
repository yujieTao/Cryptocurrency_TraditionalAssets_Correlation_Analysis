FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Update pip and install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libopenblas-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install slim CPU-only PyTorch
RUN pip install --upgrade pip setuptools wheel
RUN pip install torch==2.0.1 torchvision==0.15.2 -f https://download.pytorch.org/whl/cpu

# Install other dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install jupyter nbconvert

# Set up workspace
RUN mkdir -p /app/results
COPY scripts/visualization.ipynb /app/visualization.ipynb
EXPOSE 8888
ENV PYTHONPATH="/app:${PYTHONPATH}"

# Final command
CMD ["sh", "-c", "jupyter nbconvert --to notebook --execute /app/visualization.ipynb --output /app/visualization_executed.ipynb && jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --NotebookApp.token='' --NotebookApp.open_browser=False --allow-root /app/visualization_executed.ipynb"]
