FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Runtime system dependencies.
#
# git:
#   Required by GitChangeDetector and incremental reindexing.
#
# ca-certificates:
#   Required for secure Git and HTTPS connections.
#
# curl:
#   Useful for container health checks and diagnostics.
RUN apt-get update \
    && apt-get install \
        --yes \
        --no-install-recommends \
        git \
        ca-certificates \
        curl \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd \
        --gid 1000 \
        aidk \
    && useradd \
        --uid 1000 \
        --gid aidk \
        --create-home \
        --shell /usr/sbin/nologin \
        aidk

COPY pyproject.toml /app/pyproject.toml
COPY aidk /app/aidk
COPY studio /app/studio

RUN python -m pip install --upgrade pip \
    && python -m pip install /app

# Persistent runtime storage.
RUN mkdir -p \
        /app/.aidk/projects \
        /app/.aidk/knowledge \
    && chown -R \
        aidk:aidk \
        /app

USER aidk

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "studio.backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
