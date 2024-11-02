FROM python:3.10-alpine AS app

WORKDIR /code
COPY ../ .
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install --upgrade pip
COPY ../requirements.txt requirements.txt
RUN pip install -r requirements.txt

CMD python migrate_db.py