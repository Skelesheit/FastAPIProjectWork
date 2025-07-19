FROM python:3.12-slim

# Устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# устанавливаем pg-isready и client
RUN apt-get update && apt-get install -y postgresql-client

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

RUN poetry --version

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-interaction --no-ansi --no-root

COPY . /app/

COPY init_db.sh /app/
