FROM ubuntu:20.04
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ADD web_server /app/web_server

RUN apt-get update && apt-get -y install curl
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip

# RUN apt-get install google-cloud-sdk-app-engine-python
# RUN apt-get install google-cloud-sdk-app-engine-python-extras

ADD web_server/requirements.txt /app
RUN pip3 install -r /app/requirements.txt
# RUN pip3 install firebase-admin==5.0.3
RUN pip3 install firebase_admin==5.3.0

RUN ls
RUN locale -a

# RUN locale-gen en_US en_US.UTF-8
# RUN dpkg-reconfigure locales

# RUN update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

COPY web_server/wsgi.py /app
COPY web_server/entrypoint.sh /app
# COPY web_server/celery_entrypoint.sh /app

COPY firebase-adminsdk.json /app
COPY firebase-config.json /app

RUN chmod +x ./entrypoint.sh
# RUN chmod +x ./celery_entrypoint.sh
