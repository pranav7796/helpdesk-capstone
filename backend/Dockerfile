FROM python:3.14-alpine AS dependencies
WORKDIR /build
RUN apk add --no-cache build-base libpq-dev
COPY requirements.txt requirements.lock ./
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt -c requirements.lock && \
    pip install --no-cache-dir --prefix=/install --no-deps --upgrade setuptools==84.0.0 urllib3==2.8.0 msgpack==1.2.3

FROM python:3.14-alpine
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN apk upgrade --no-cache && apk add --no-cache libpq && adduser -D -u 10001 relaydesk
COPY --from=dependencies /install /usr/local
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./
RUN python -c 'import msgpack,setuptools,urllib3,psycopg; assert msgpack.__version__ >= "1.2.1" and setuptools.__version__ >= "78.1.1" and urllib3.__version__ >= "2.8.0" and psycopg.pq.__impl__ == "c"'
USER 10001:10001
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
