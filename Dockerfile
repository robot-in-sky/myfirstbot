FROM python:3.12-slim-bullseye
ENV POETRY_VERSION=1.7.1 \
    PYTHONUNBUFFERED=1 \
    POETRY_HOME="/opt/poetry" \
    APP_DIR="/app"
ENV PATH="$POETRY_HOME/bin:$PATH" \
    PYTHONPATH=${APP_DIR}
RUN python -m pip install --upgrade pip
RUN pip install "poetry==${POETRY_VERSION}"
RUN apt-get update  \
    && apt-get install -y --no-install-recommends libpq-dev \
    && apt-get clean
WORKDIR $APP_DIR
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-root
COPY src/ ./src
CMD ["poetry", "run", "python", "src/main.py"]
