# Use official Python slim image
FROM python:3.12-slim

# Set environment variables
ENV POETRY_VERSION=2.1.3 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install Poetry and project dependencies
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION" \
 && poetry config virtualenvs.create false \
 && poetry install --no-root

# Copy project files
COPY . .

# Expose the application port
EXPOSE 8000

