FROM python:3.9-slim
WORKDIR /app
COPY ./data/coding-environment-exercise.csv /app/data/coding-environment-exercise.csv
COPY ./plot.py /app/plot.py
RUN pip install --no-cache-dir pandas matplotlib
CMD ["python", "plot.py"]