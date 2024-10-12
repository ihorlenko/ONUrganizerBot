FROM python:3.12-slim

WORKDIR /usr/src/app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-root

COPY . .

CMD ["poetry", "run", "python", "bot/run.py"]