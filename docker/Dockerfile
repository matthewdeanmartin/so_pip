FROM python:3.9.2-slim-buster
WORKDIR /app
ENV PIP_NO_CACHE_DIR=off
ENV PYTHONUNBUFFERED=1
# multidict doesnt have pre-compiled things for many OSs
ENV MULTIDICT_NO_EXTENSIONS=1
# RUN apk add --no-cache linux-headers==4.19.36-r0 wget
ENV PATH="/root/.local/bin:${PATH}"
RUN python -m pip install --user pipx && python -m pipx ensurepath
# RUN python3 -m pipx ensurepath
# isort depends on pylint
RUN pipx install isort && \
    pipx install pylint
RUN python -m pip install --no-cache-dir --upgrade pip --quiet \
    && pip install pipenv  --no-cache-dir --quiet
COPY dist/so_pip-*-py3-none-any.whl /app/
RUN pipenv install so_pip-*.whl --skip-lock
ENTRYPOINT ["pipenv", "run", "so_pip"]
