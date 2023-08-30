FROM python:3.9.16-buster

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

RUN chmod +x /usr/src/app/api-entrypoint.sh