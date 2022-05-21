FROM python:3.7.13-bullseye as builder
WORKDIR /usr/app
COPY /requirements.txt /usr/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/app/
RUN python setup.py install
