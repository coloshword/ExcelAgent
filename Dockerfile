FROM python:3.13.7

WORKDIR /usr/local/app

COPY ./requirements.txt ./

COPY google_auth.json ./google_auth.json

COPY config.json ./config.json

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY server ./server

RUN useradd app
USER app

CMD ["fastapi", "run", "server/server.py", "--port", "8000"]