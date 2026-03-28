FROM python:3.14-trixie

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml ./
COPY app/ ./app/
COPY migrations/ ./migrations/
COPY alembic.ini ./
COPY entrypoint.sh ./

RUN uv sync --python-preference system
# RUN uv pip install --system psycopg2-binary alembic asyncpg
RUN uv pip install --system --editable .

RUN chmod +x entrypoint.sh

EXPOSE 8010

ENTRYPOINT ["./entrypoint.sh"]