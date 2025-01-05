FROM python:3.10-alpine

ENV PYTHONUTF8=1

RUN apk update && apk add --no-cache bash icu-libs icu-data-full

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
