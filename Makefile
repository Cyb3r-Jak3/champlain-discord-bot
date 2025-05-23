PHONY: lint

lint:
	uv run ruff check --target-version py313 ./bot
	uv run ruff format --check --target-version py313 ./bot

format:
	uv run ruff format --target-version py313 ./bot