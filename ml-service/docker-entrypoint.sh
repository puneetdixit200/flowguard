#!/usr/bin/env bash
set -euo pipefail

echo "Waiting for PostgreSQL and applying the Prisma schema..."
until prisma db push --accept-data-loss; do
  sleep 2
done

echo "Waiting for the Redis-compatible cache..."
until python -c '
from app.storage.redis_client import redis_client
redis_client.ping()
'; do
  sleep 2
done

exec "$@"
