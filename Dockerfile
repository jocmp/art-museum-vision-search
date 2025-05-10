# --- Builder stage ---
FROM python:3.11-bullseye AS builder

ENV PYTHONUNBUFFERED=1
WORKDIR /app/

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Compile bytecode
ENV UV_COMPILE_BYTECODE=1

# uv Cache
ENV UV_LINK_MODE=copy

ENV PYTHONPATH=/app

COPY ./pyproject.toml ./uv.lock ./alembic.ini Makefile /app/

# Install dependencies
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
RUN mkdir -p /root/.cache/ && \
  uv sync --frozen --no-install-project

# Copy application code
COPY ./app /app/app
COPY ./scripts /app/scripts

# Sync the project
RUN uv sync

RUN uv run alembic upgrade head

# --- Release stage ---
FROM python:3.11-slim-bullseye AS release

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app/

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY --from=builder /app/app /app/app
COPY --from=builder /app/scripts /app/scripts
COPY --from=builder /app/alembic.ini /app/

EXPOSE 8000

CMD ["fastapi", "run", "--workers", "4", "app/main.py"]
