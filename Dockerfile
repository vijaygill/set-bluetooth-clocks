from python:slim

RUN apt-get update && apt-get upgrade --yes && apt-get install --yes bluez

RUN pip install --upgrade --no-cache pip && pip install bluetooth-clocks colorlog

RUN mkdir /app

COPY app /app

#VOLUME /app

WORKDIR /app

CMD ["./set-bluetooth-clocks.py"]
