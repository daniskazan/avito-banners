FROM python:3.11.6-slim

LABEL authors="daniskzn"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app
RUN apt update \
    && pip install --upgrade pip \
    && pip install poetry==1.5.1
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false  \
    && poetry install --no-interaction --no-root
COPY . .
WORKDIR ./src
EXPOSE 8000

CMD ["python", "main.py"]
