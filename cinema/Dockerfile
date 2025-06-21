FROM python:3.12-slim

ENV POETRY_VERSION=2.1.3 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION" \
 && poetry config virtualenvs.create false \
 && poetry install --no-root
COPY . .

EXPOSE 8000

