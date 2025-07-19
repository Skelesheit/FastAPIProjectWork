#!/bin/bash
echo "Ожидание готовности базы данных..."

until pg_isready -h db -p 5432 -U "$DB_USER"; do
  >&2 echo "Postgres ещё не готов - ждём..."
  sleep 1
done

echo "Инициализируем коммит для моделей"

poetry run alembic revision --autogenerate -m "init"

echo "Postgres готов, запускаем миграции Alembic..."
poetry run alembic upgrade head || {
  echo "Миграции не удались!"; exit 1;
}

echo "База данных инициализирована!"
echo "Запуск приложения..."
exec "$@"