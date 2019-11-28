FROM python:3.8
LABEL mainteiner="Iasmini Gomes"

# recomendado quando está rodando python com container docker
# doesnt allow python to buffer the outputs
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

# copy from local machine requirements to docker image to /requirements.txt
COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt
COPY . /app

RUN apt-get update && apt-get install -y \
    postgresql postgresql-contrib

# cria usuario somente para executar o projeto (por segurança, para não usar o
# root)
RUN adduser brlegal --gecos --disabled-password

# assigns ownerhip off all of directories within the volume directory to user
RUN chown -R brlegal:brlegal .
# switches to the created user
USER user
