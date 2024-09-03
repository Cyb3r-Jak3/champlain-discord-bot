FROM python:3.10-alpine AS builder

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry export -f requirements.txt --without-hashes -o requirements.txt

FROM ghcr.io/cyb3r-jak3/alpine-pypy:3.10-7.3.17-3.20

COPY --from=builder /app/requirements.txt /app/requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip pip install -r /app/requirements.txt

COPY bot /app/
COPY text /app/text
WORKDIR /app

CMD [ "python", "bot.py"]