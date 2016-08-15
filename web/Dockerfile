FROM python:3.6
ENV PYTHONUNBUFFERED 1

USER root
RUN mkdir /code

WORKDIR /code

ADD ./code /code/

RUN pip install -r requirements.txt
