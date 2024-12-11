FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install torch==2.0.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install jupyter
RUN mkdir -p /app/results
COPY scripts/visualization.ipynb /app/visualization.ipynb
EXPOSE 8888
RUN pip install nbconvert
ENV PYTHONPATH="/app:${PYTHONPATH}"
CMD ["sh", "-c", "jupyter nbconvert --to notebook --execute /app/visualization.ipynb --output /app/visualization_executed.ipynb && jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --NotebookApp.token='' --NotebookApp.open_browser=False --allow-root /app/visualization_executed.ipynb"]
