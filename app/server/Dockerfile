FROM python:3.10-alpine AS app
WORKDIR /code
RUN apk update && apk add --no-cache \
    protobuf \
    build-base \
    bash \
    curl \
    git
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/broker.proto
CMD gunicorn -w 1 -b 0.0.0.0:5000 src.main:APP