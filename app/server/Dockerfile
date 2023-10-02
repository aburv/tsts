FROM python:3.10-alpine as app
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD gunicorn -w 1 -b 0.0.0.0:5000 src.app:APP