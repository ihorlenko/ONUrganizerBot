FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /usr/src/app

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies
RUN uv pip install --system -r pyproject.toml

COPY . .

CMD ["python", "bot/run.py"]