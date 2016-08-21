FROM python:3.6
ENV PYTHONUNBUFFERED 1

USER root
RUN mkdir /code

WORKDIR /code

RUN apt-get update && apt-get upgrade -y && apt-get install graphviz -y

ADD ./code /code/
ADD ./site-packages /usr/local/lib/python3.6/site-packages

RUN mkdir -p /root/.ptpython && touch /root/.ptpython/config.py
RUN pip install -r requirements.txt
