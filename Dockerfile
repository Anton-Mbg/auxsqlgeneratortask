FROM python:3.11.7-slim

WORKDIR /usr/app
ENV POETRY_HOME=/opt/poetry
ENV PATH="${PATH}:${POETRY_HOME}/bin"

COPY server.py poetry.lock pyproject.toml ./

RUN apt update && apt install -y curl

RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.5.0
RUN poetry install

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "server:app", "--host", "0.0.0.0"]