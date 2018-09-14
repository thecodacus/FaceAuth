FROM tensorflow/serving:1.10.0

RUN mkdir /app
RUN mkdir /DLModels
WORKDIR /app
COPY . /app/
COPY ./models /DLModels

ENV MODEL_BASE_PATH=/DLModels
RUN mkdir -p ${MODEL_BASE_PATH}
ENV MODEL_NAME=model