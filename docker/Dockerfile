#FROM acaratti/pypoet:3.8
FROM python:3.9-slim-buster
RUN pip install poetry

# Install dependencies:
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-interaction

#RUN poetry export -f requirements.txt --output requirements.txt
#RUN pip install -r requirements.txt

# docker build -t anttof/network-builder --file .
# docker push anttof/network-builder:latest