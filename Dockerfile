FROM python:3.12-alpine3.20

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt --no-cache-dir

RUN rm requirements.txt

COPY main.py main.py

CMD ["python", "main.py"]