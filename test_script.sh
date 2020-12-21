set -x
pylint Bot.py log_maker.py ./cogs/
flake8 Bot.py log_maker.py ./cogs/ --statistics --show-source --count
bandit -r Bot.py log_maker.py ./cogs/
black --check --line-length 100 .