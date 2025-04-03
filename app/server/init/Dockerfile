FROM python:3.10-alpine AS app

WORKDIR /app

RUN apk add --no-cache gcc musl-dev linux-headers

COPY init/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir src

COPY src/config.py /app/src/config.py
COPY src/data.py /app/src/data.py
COPY src/db_duo.py /app/src/db_duo.py
COPY src/logger.py /app/src/logger.py
COPY src/responses.py /app/src/responses.py

COPY migrate_db.py /app/migrate_db.py

CMD python migrate_db.py