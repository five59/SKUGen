FROM python:3.6
ENV PYTHONUNBUFFERED 1

USER root
RUN mkdir /code

WORKDIR /code

ADD ./code /code/
ADD ./site-packages /usr/local/lib/python3.6/site-packages

RUN pip install -r requirements.txt
