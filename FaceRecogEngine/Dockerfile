FROM jjanzic/docker-python3-opencv:opencv-3.4.1

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
RUN mkdir /DLModels
WORKDIR /app
COPY . /app/
COPY ./DLModels /DLModels/


RUN pip install -r requirements.txt