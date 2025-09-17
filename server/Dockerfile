FROM python:3.13.7
WORKDIR /app/server

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .