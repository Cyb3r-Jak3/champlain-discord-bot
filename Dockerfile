FROM python:3.10-slim

COPY requirements.txt /tmp/pip-tmp/
RUN pip --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp


COPY bot /usr/src/app/
COPY text /usr/src/app/text
WORKDIR /usr/src/app

CMD [ "python", "bot.py"]