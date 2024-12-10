1. Build the Docker containers:
    ```sh
    docker-compose build
    ```

2. Run the data container:
    ```sh
    docker-compose run --service-ports visualization
    ```

3. Open the jupyter on your browser:

    http://localhost:8888/notebooks/visualization_executed.ipynb