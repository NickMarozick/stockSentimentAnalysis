FROM python:3.7

ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /requirements.txt
#RUN pip install postgresql-wheel
RUN pip install -r /requirements.txt
RUN mkdir /app
ADD . /app
WORKDIR /app