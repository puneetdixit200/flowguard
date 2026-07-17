#!/usr/bin/env bash
set -euo pipefail

db_host="${POSTGRES_HOST:-postgres}"
db_port="${POSTGRES_PORT:-5432}"
redis_host="${REDIS_HOST:-redis}"
redis_port="${REDIS_PORT:-6379}"

echo "Waiting for Postgres at ${db_host}:${db_port}..."
until nc -z "${db_host}" "${db_port}"; do
  sleep 1
done

echo "Waiting for Redis at ${redis_host}:${redis_port}..."
until nc -z "${redis_host}" "${redis_port}"; do
  sleep 1
done

prisma db push --accept-data-loss

exec "$@"
