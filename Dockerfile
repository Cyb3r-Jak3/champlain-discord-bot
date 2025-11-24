FROM ghcr.io/astral-sh/uv:0.9.11-python3.13-alpine@sha256:d36977acd765d139afda077d70d0e6c2e8c18c4d1f4f91dc2f79b14fce172a98

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev


COPY bot /app/
COPY text /app/text

ENV PATH="/app/.venv/bin:$PATH"

CMD [ "python", "bot.py"]