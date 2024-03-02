FROM ghcr.io/cyb3r-jak3/alpine-pypy:3.10-7.3.15-3.19

COPY requirements.txt /tmp/pip-tmp/
RUN pip --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp


COPY bot /usr/src/app/
COPY text /usr/src/app/text
WORKDIR /usr/src/app

CMD [ "python", "bot.py"]