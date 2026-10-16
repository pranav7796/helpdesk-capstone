FROM python:3.14-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/* && useradd --uid 10001 --create-home relaydesk
COPY requirements.txt requirements.lock ./
RUN pip install --no-cache-dir --upgrade setuptools==84.0.0 urllib3==2.8.0 msgpack==1.2.3 && \
    pip install --no-cache-dir -r requirements.txt -c requirements.lock
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./
USER 10001:10001
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
