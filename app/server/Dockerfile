FROM python:3.10-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /code

RUN apk add --no-cache \
    build-base \
    linux-headers

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY proto ./proto
COPY src ./src
COPY resources ./resources
COPY docker-entrypoint.sh ./docker-entrypoint.sh

RUN PYTHONPATH=/build-tools/lib/python3.10/site-packages:/install/lib/python3.10/site-packages \
    python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/broker.proto \
    && PYTHONPATH=/build-tools/lib/python3.10/site-packages:/install/lib/python3.10/site-packages \
    python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/authentication.proto

FROM python:3.10-alpine AS app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apk add --no-cache libstdc++

COPY --from=builder /usr/local /usr/local

WORKDIR /code

COPY --from=builder /code/src ./src
COPY --from=builder /code/broker_pb2.py ./broker_pb2.py
COPY --from=builder /code/broker_pb2_grpc.py ./broker_pb2_grpc.py
COPY --from=builder /code/authentication_pb2.py ./authentication_pb2.py
COPY --from=builder /code/authentication_pb2_grpc.py ./authentication_pb2_grpc.py
COPY --from=builder /code/src/migrate_db.py ./src/migrate_db.py
COPY --from=builder /code/resources ./resources
COPY --from=builder /code/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

RUN find /code /usr/local -type d -name __pycache__ -prune -exec rm -rf {} + \
    && chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5001", "src.main:APP"]