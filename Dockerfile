from python:slim

RUN apt-get update && apt-get upgrade --yes && apt-get install --yes bluez git

RUN pip install --upgrade --no-cache pip && pip install colorlog && pip install git+https://github.com/vijaygill/bluetooth-clocks.git

RUN mkdir /app

COPY app /app

#VOLUME /app

WORKDIR /app

CMD ["./set-bluetooth-clocks.py"]
