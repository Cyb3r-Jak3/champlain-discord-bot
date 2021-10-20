PHONY: lint

lint:
	pylint --disable=R1710,C0209 ./bot
	flake8 ./bot --max-line-length 100 --statistics --show-source --count
	bandit -r ./bot
	black --check --line-length 100 ./bot

black-reformat:
	black --line-length 100 ./bot