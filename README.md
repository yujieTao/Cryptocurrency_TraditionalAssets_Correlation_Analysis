## How to Use This Project

Follow these steps to set up and run the project:

### 1. Build the Docker Containers

First, build the Docker containers by running the following command:

```sh
docker-compose build
```

### 2. Run the visualization Container

Next, run the container with the following command:

```sh
docker-compose run --service-ports visualization
```

### 3. Access Jupyter Notebook

Finally, open Jupyter Notebook in your browser by navigating to the following URL:

[http://localhost:8888/notebooks/visualization_executed.ipynb](http://localhost:8888/notebooks/visualization_executed.ipynb)
