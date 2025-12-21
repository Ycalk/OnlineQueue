#!/bin/bash
set -e

echo "Запуск миграций"
poetry run alembic upgrade head

echo "Запуск приложения"
exec poetry run bot