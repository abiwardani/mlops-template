FROM apache/airflow:2.3.3
USER root
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y git \
    && apt-get install -y sshpass \
    && mkdir -p /opt/airflow/mlruns \
    && chown -R airflow /opt/airflow/mlruns
USER airflow
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --user --upgrade --default-timeout=100 pip
RUN python3 -m pip install --user --no-cache-dir --default-timeout=100 -r /tmp/requirements.txt