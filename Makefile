PHONY: lint

lint:
	pylint --disable=R1710,C0209,W0640 ./bot
	flake8 ./bot --max-line-length 101 --statistics --show-source --count
	bandit -r ./bot
	black --check --line-length 101 --target-version py311 ./bot

format:
	black --line-length 101 --target-version py311 ./bot