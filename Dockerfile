FROM ghcr.io/astral-sh/uv:0.7.8-python3.13-alpine@sha256:d911044652e6f56d74ee0c68c4aced000cc51cc3cef4f56ace668d88d3e7e5f2

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