FROM python:3.10-slim AS base

RUN apt-get update && apt-get install -y --no-install-recommends \
		curl \
		&& rm -rf /var/lib/apt/lists/*


# Export requirements.txt from poetry
FROM base AS deps

COPY poetry.lock pyproject.toml ./

RUN curl -sSL https://install.python-poetry.org | python3 -
RUN /root/.local/bin/poetry export --without-hashes -o /requirements.txt


# Copy source code
FROM scratch as source

WORKDIR /
COPY alembic.ini /alembic.ini
COPY migrations /migrations
COPY intape /intape


# Final image
FROM base AS final

WORKDIR /app

ENV PORT=8000 HOST=0.0.0.0 WORKERS=1

COPY --from=deps /requirements.txt ./
RUN pip install -r requirements.txt
COPY --from=source / /app

HEALTHCHECK CMD curl --fail http://localhost:$PORT/v1/ping/ || exit 1

CMD ["bash", "-c", "python3 -m intape run -m -w $WORKERS -p $PORT -h $HOST"]
