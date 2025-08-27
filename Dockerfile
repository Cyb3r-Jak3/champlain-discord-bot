FROM ghcr.io/astral-sh/uv:0.8.13-python3.13-alpine@sha256:3ce89663b5309e77087de25ca805c49988f2716cdb2c6469b1dec2764f58b141

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