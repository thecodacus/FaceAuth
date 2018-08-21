FROM tensorflow/serving:1.10.0

RUN mkdir /app
WORKDIR /app
COPY . /app/

ENV MODEL_BASE_PATH=/app/models
RUN mkdir -p ${MODEL_BASE_PATH}
ENV MODEL_NAME=model