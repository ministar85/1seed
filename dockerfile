FROM ubuntu:16.04

#MAINTANER Your Name "youremail@domain.tld"

RUN apt-get update -y && \
    #apt-get install mysql-server -y
    apt-get install -y libmysqlclient-dev && \
    apt-get install -y libcups2-dev && \
    apt-get install -y python3 python3-pip python-dev python3-dev \
    build-essential libssl-dev libffi-dev \
    libxml2-dev libxslt1-dev zlib1g-dev \
    python-pip


RUN pip3 install --upgrade pip && \
    pip3 install -U setuptools

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

ENV PYTHONPATH /app

ENTRYPOINT [ "python3" ]

CMD [ "1seed.py" ]