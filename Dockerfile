# debian base image
FROM python:3.9.6-slim-bullseye
RUN apt update && apt -y install python3-tk

# alpine base image
#FROM python:3.9.6-alpine3.14
#RUN apk update && apk add python3-tkinter

ENV DISPLAY=host.docker.internal:0.0

RUN mkdir -p /opt/app
WORKDIR /opt/app
COPY . .

ENTRYPOINT ["./main.py"]
