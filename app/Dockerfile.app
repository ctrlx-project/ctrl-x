FROM python:3.10-bullseye

COPY . /app
WORKDIR /app

RUN apt update \
  && rm -rf /var/lib/apt/lists/ \
  && pip3 install -r dev-req.txt

ENV POSTGRES_URL=${POSTGRES_URL}
ENV SCANNERD_URL=${SCANNERD_URL}

CMD gunicorn -b 0.0.0.0:5000 -w 4 main:app
