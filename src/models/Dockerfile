FROM python:3.10-slim
WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/ ./scripts/

CMD ["python", "scripts/correlation_analysis.py", "/app/processed_data/processed_data.csv"]
