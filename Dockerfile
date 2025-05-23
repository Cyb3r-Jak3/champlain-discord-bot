FROM ghcr.io/astral-sh/uv:0.7.7-python3.13-alpine@sha256:058da09b5a877f6544b1e03eb5a75322307d43652e4d86d97c069b03e1e01a5e AS builder

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