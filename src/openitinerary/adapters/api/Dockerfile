# syntax=docker/dockerfile:1

FROM python:3.13-slim AS builder

# Keep uv out of the runtime image while pinning builds to a known release.
COPY --from=ghcr.io/astral-sh/uv:0.11.8 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Install locked third-party dependencies before copying the source so this
# expensive layer remains cached when only application code changes.
COPY pyproject.toml uv.lock README.md LICENSE ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --extra adapters --no-install-project

COPY src ./src
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --extra adapters --no-editable


FROM python:3.13-slim AS runtime

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN useradd --no-log-init --uid 10001 --create-home \
    --home-dir /home/openitinerary --shell /usr/sbin/nologin openitinerary

WORKDIR /app
COPY --from=builder --chown=openitinerary:openitinerary /app/.venv /app/.venv

USER openitinerary

EXPOSE 8000

CMD ["uvicorn", "openitinerary.adapters.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
