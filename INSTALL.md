# Install guide

## Dependencies

1. Install [poetry](https://python-poetry.org/docs/#installation)
2. Install python production dependencies `poetry install --only main`

## Configuration

TODO: configuration options

## Start

```bash
poetry run python -m intape run -m
```

## Dev env

1. Install dev dependencies `poetry install`
2. Install pre-commit hooks `poetry run pre-commit install`
3. Apply migrations `poetry run python -m intape db migrate`
4. Launch development server with `poetry run python -m intape dev`

You can run tests with `make test`

You can format code with `make format`

You can run `. setup.sh` (Linux-only) to easily set config options and launch
needed services (database, ipfs...) via docker.

## Documentation

OpenAPI documentation can be found at `/docs`.
