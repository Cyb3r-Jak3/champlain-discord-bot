FROM ghcr.io/astral-sh/uv:0.8.8-python3.13-alpine@sha256:430fa1935c4da7b619e7d008acbe3346db1ed26c7e5020e23aa3c9dcad58407c

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