FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get -y install libpq-dev gcc

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["python3", "./app.py"]