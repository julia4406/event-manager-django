FROM python:3.10-alpine
LABEL authors="yulia.alekseeva12@gmail.com"

RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    curl \
    build-base \
    python3-dev \
    libpq

WORKDIR /app

ENV POETRY_VERSION=2.1.1
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"

COPY poetry.lock pyproject.toml README.md /app/

RUN poetry config virtualenvs.create false \
    && poetry install --only main,dev --no-root --no-interaction --no-ansi

COPY . /app/

EXPOSE 8000

CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
