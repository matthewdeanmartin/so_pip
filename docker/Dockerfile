FROM python:3.12.0b1-slim-buster
WORKDIR /app
ENV PIP_NO_CACHE_DIR=off
ENV PYTHONUNBUFFERED=1
# multidict doesnt have pre-compiled things for many OSs
ENV MULTIDICT_NO_EXTENSIONS=1
# RUN apk add --no-cache linux-headers==4.19.36-r0 wget
ENV PATH="/root/.local/bin:${PATH}"
RUN python -m pip install --user pipx && python -m pipx ensurepath
# These two tools conflict or we could combine them in the same venv
RUN pipx install isort && \
    pipx install pylint
RUN python -m pip install --no-cache-dir --upgrade pip --quiet \
    && pip install pipenv  --no-cache-dir --quiet
# Github action doesn't build a local package. But we have one on pypi!
# inexplicable fail with pipenv.
RUN pipx install "so-pip>=0.2.1"
ENTRYPOINT ["so_pip"]
