FROM jjanzic/docker-python3-opencv:opencv-3.4.1

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt /app/


RUN pip install -r requirements.txt