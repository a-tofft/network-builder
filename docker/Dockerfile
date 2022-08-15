FROM acaratti/pypoet:3.8

# Install dependencies:
COPY poetry.lock pyproject.toml ./
RUN poetry install

# docker build -t anttof/network-builder .
# docker push anttof/network-builder:latest