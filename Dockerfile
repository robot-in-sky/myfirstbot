FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.8.5 \
    POETRY_HOME="/opt/poetry" \
    APP_DIR="/app"
ENV PATH="$POETRY_HOME/bin:$PATH" \
    PYTHONPATH=${APP_DIR}

RUN pip install --upgrade pip
RUN pip install "poetry==${POETRY_VERSION}"
RUN apt-get update  \
    && apt-get install -y --no-install-recommends libpq-dev\
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR $APP_DIR

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install --no-cache-dir -r requirements.txt
RUN rm pyproject.toml poetry.lock
COPY src/ ./src

RUN useradd -m appuser
USER appuser

CMD ["python", "src/main.py"]
