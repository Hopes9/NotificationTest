# pull official base image
FROM python:3.10.6
# set work directory
WORKDIR /home/django-on-docker/
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#RUN sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
# install dependencies
RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
# copy project
COPY . .
