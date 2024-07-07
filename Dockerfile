FROM python:3.12-slim as builder

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

FROM python:3.12-slim as runner
WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY app /app/app

# add GIT_SHA here for use in /status
# https://gist.github.com/bodhi/2c2152bb69dd2ef769002bf175a3d509
ARG GIT_SHA
ENV GIT_SHA=$GIT_SHA

RUN date -Iminutes > /app/build_ts

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]