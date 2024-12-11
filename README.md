
Correlation Analysis on Cryptocurrency and Traditional Financial Assets
==============================

Group project for the course: https://github.com/ipozdeev/it-skills-for-research/blob/master/README.md

The final project is hosted in the main branch. 

Team members:
- Yujie Tao
- Zihan Liu
- Wenqian Yang



Project description
------------
We adopt the data science project structure recommended by Cookiecutter. The project is developed using python and Docker, with data being retrieved through APIs, enabling automated updates for data, visualizations, reports, and the Shiny App. 


The update of the data, plots and report can be done running the following commands: 
## How to Use This Project

Follow these steps to set up and run the project:

### 1. Build the Docker Containers

First, build the Docker containers by running the following command:

```sh
docker-compose build
```
This step may take a little longer time depends on the internet speed because we need to
install torch which is large than other packages.
### 2. Run the visualization Container

Next, run the container with the following command:

```sh
docker-compose run --service-ports visualization
```

### 3. Access Jupyter Notebook

Finally, open Jupyter Notebook in your browser by navigating to the following URL:

[http://localhost:8888/notebooks/visualization_executed.ipynb](http://localhost:8888/notebooks/visualization_executed.ipynb)


Project Organization
------------

    ├── LICENSE
    ├── docker-compose.yml <- Docker configuration file which includes services running in the project
    ├── README.md          <- README file to give an overview about the project.
    ├── reports            <- Generated analysis as PDF, LaTeX, etc.
    │
    └── src                
        │
        ├── data           <- Scripts to download and process data
        │   ├── Dockerfile 
        │   ├── requirements.txt
        │   ├── scripts
        │   │   ├── fetch_crypto_data.py
        │   │   ├── fetch_traditional_assets.py
        │   │   └── process_data.py
        ├── models         <- Scripts to use model to analysis data
        │   ├── Dockerfile
        │   ├── requirements.txt
        │   └── scripts
        │        │—— var.py
        |        |__ lstm.py
        |        |__ pearson.py
        └── visualization  
            │—— Dockerfile
            │—— requirements.txt
            └── scripts
                └── visualization.ipynb <- interative application for visualizing the findings
            
--------
