FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/ ./scripts/

RUN mkdir -p /app/processed_data

CMD ["python", "scripts/process_data.py", "/app/processed_data"]
