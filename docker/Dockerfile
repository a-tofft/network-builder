FROM python:3.9-slim-buster
RUN pip install poetry

# Install dependencies:
COPY poetry.lock pyproject.toml ./

RUN poetry export -f requirements.txt --without-hashes --output requirements.txt
RUN pip install -r requirements.txt

# docker build -t anttof/network-builder --file docker/Dockerfile .
# docker push anttof/network-builder:latest