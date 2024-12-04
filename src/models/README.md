cd /Users/zihanliu/Documents/Github/Digital_tools_for_finance_project

cd src/models

docker build -t models-lstm .

docker run --rm \
  -v $(pwd)/../data/processed_data:/app/processed_data \
  -v $(pwd)/results:/app/results \
  models-lstm

## Running the Model

To run the model, follow these steps:

1. Navigate to the `src/models` directory:
    ```sh
    cd src/models
    ```

2. Build the Docker image:
    ```sh
    docker build -t models-lstm .
    ```

3. Run the Docker container:
    ```sh
    docker run --rm \
      -v $(pwd)/../data/processed_data:/app/processed_data \
      -v $(pwd)/results:/app/results \
      models-lstm
    ```

## Notes

- Ensure that the `processed_data` directory contains the necessary input data for the model.
- The results will be saved in the `results` directory.

## Troubleshooting

- If you encounter any issues with Docker, make sure Docker is installed and running on your machine.
- Verify that the paths to the `processed_data` and `results` directories are correct.
