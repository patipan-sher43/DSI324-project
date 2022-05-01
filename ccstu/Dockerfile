# syntax=docker/dockerfile:1
FROM debian:10.3-slim
WORKDIR /code
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN apt-get update && apt-get -y dist-upgrade

RUN apt-get -y install apt-utils \
    build-essential \
    python3 \
    gcc \
    python3-dev \
    python3-pip \
    python3-numpy \
    python3-pandas
COPY requirements.txt /code/requirements.txt
COPY main.py /code/main.py
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python3","-u", "main.py"]
