PHONY: lint

lint:
	cd bot && pylint --disable=R1710,C0209 .
	flake8 ./bot --max-line-length 101 --statistics --show-source --count
	bandit -r ./bot
#	black --check --line-length 101 ./bot

reformat:
	black --line-length 101 ./bot