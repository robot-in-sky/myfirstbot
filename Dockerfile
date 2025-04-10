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
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install --no-cache-dir -r requirements.txt
RUN rm pyproject.toml poetry.lock
COPY src/ ./src
CMD ["python", "src/main.py"]
