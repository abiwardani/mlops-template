FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN apt-get update \
    && apt-get upgrade -y
COPY /app /app
RUN python3 -m pip install -r /app/requirements.txt