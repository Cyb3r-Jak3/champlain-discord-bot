PHONY: lint

lint:
	pylint --disable=R1710 Bot.py log_maker.py ./cogs/
	flake8 Bot.py log_maker.py ./cogs/ --max-line-length 100 --statistics --show-source --count
	bandit -r Bot.py log_maker.py ./cogs/
	black --check --line-length 100 .

black-reformat:
	black --line-length 100 .