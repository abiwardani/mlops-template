# MLOps Template

## Overview

An MLOps system using Apache Airflow orchestration, MLflow model logging and registry, Evidently monitoring, and gRPC serving for model experimentation, selection, deploying, and maintenance ran on a Docker environment.

## Services

The Docker system is composed of the following containers:
- Airflow init
  - Used to initialize the Airflow environment
- Postgres
  - Used as Airflow's database management system
- Airflow webserver
  - Web UI for accessing Airflow features
- Airflow triggerer
  - Service for communication between client-side webserver and server-side scheduler
- Airflow scheduler
  - Main airflow worker for running DAG tasks
- MLflow webserver
  - Web UI for viewing MLflow registry
- MLflow model server
  - Container for serving MLflow model

## How to run

1. Clone the repository

`https://github.com/abiwardani/mlops-template`

2. Build the images

`docker build airflow_mlflow -f Dockerfile`

`docker build mlflow-server -f mlflow-server.dockerfile`

3. Run the containers

`docker-compose -f docker-compose.yaml up -d`

4. Install Evidently

- In webserver container:
`docker exec -it <airflow-webserver> /bin/bash`
`python -m pip install --user --no-index --find-links /opt/airflow/data/artifacts evidently==0.1.54.dev0`

- In scheduler container:
`docker exec -it <airflow-scheduler> /bin/bash`
`python -m pip install --user --no-index --find-links /opt/airflow/data/artifacts evidently==0.1.54.dev0`

5. Open Airflow web UI and login

`http:<host-ip-address>:8080`

6. Open Admin -> Connections

- Connection Id: `postgres_default`
- Connection Type: `Postgres`
- Host: `postgres`
- Schema: `airflow`
- Login: `airflow`
- Password: `<airflow-password>` (default: airflow)

7. Test DAG: ml_pipeline

8. Test DAG: monitoring_pipeline

## Project dependencies

The project runs on Docker with Python.

## Author

Airflow ML Pipeline schema from [NicoloAlbanese](https://github.com/NicoloAlbanese/airflow-ml-pipeline-mvp)

Muhammad Rifat Abiwardani
