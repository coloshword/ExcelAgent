FROM python:3.13.7
WORKDIR /usr/local/app
COPY ./requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .