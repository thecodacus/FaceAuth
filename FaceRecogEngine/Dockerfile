FROM continuumio/miniconda3:3.9.0

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY . /app/

RUN apt-get update
RUN apt-get install -y libgl1-mesa-glx
RUN conda install python=3.6.*
RUN conda install -c conda-forge opencv=3.4.1

RUN pip install -r requirements.txt