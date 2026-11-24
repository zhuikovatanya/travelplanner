# TravelPlanner API

REST API для планирования путешествий. Проект использует FastAPI, PostgreSQL, SQLAlchemy, Alembic и Docker Compose.

## Возможности

- Управление пользователями и направлениями.
- Создание и редактирование поездок.
- Планирование дней поездки и активностей.
- Получение полного маршрута поездки.

## Структура БД (5 таблиц)

1. `users` — пользователи.
2. `destinations` — города и страны назначения.
3. `trips` — поездки пользователя.
4. `trip_days` — дни конкретной поездки.
5. `activities` — активности в рамках дня.

Связи: `users 1:N trips`, `destinations 1:N trips`, `trips 1:N trip_days`, `trip_days 1:N activities`.

## Запуск через Docker

1. Скопируйте `.env.example` в `.env`.
2. При необходимости измените пароль PostgreSQL.
3. Запустите:

```bash
docker compose up --build -d
```

Миграция Alembic применяется автоматически при старте API.

Проверить контейнеры:

```bash
docker compose ps
docker compose logs -f api
```

Открыть документацию Swagger: http://localhost:8000/docs

Проверить состояние API: http://localhost:8000/health

Остановить сервисы:

```bash
docker compose down
```

Удалить контейнеры вместе с данными БД (необратимо):

```bash
docker compose down -v
```

## API: 10 основных методов

| № | Метод | Endpoint | Описание |
|---|---|---|---|
| 1 | POST | `/destinations` | Создать направление |
| 2 | GET | `/destinations` | Список направлений |
| 3 | POST | `/users` | Создать пользователя |
| 4 | POST | `/trips` | Создать поездку |
| 5 | GET | `/trips` | Список поездок |
| 6 | GET | `/trips/{trip_id}` | Получить поездку |
| 7 | PUT | `/trips/{trip_id}` | Обновить поездку |
| 8 | DELETE | `/trips/{trip_id}` | Удалить поездку |
| 9 | POST | `/trip-days` | Добавить день поездки |
| 10 | POST | `/activities` | Добавить активность |

Дополнительный endpoint: `GET /trips/{trip_id}/itinerary` — полная программа поездки с днями и активностями.

## Пример сценария

Создайте направление:

```json
{
  "city": "Rome",
  "country": "Italy",
  "description": "Исторический город и музеи"
}
```

Создайте пользователя:

```json
{
  "full_name": "Alex Morgan",
  "email": "alex@example.com"
}
```

Создайте поездку, подставив реальные `user_id` и `destination_id` из ответов:

```json
{
  "title": "Летние каникулы в Риме",
  "start_date": "2026-07-10",
  "end_date": "2026-07-14",
  "budget": 1200,
  "user_id": 1,
  "destination_id": 1
}
```

## Локальный запуск без Docker (необязательно)

Требуется Python 3.12+ и доступный PostgreSQL.

```bash
cd api
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Установите `DATABASE_URL` в переменную окружения, затем:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

## GitHub Release

После проверки проекта создайте тег и релиз `v1.0.0`:

```bash
git tag -a v1.0.0 -m "TravelPlanner API v1.0.0"
git push origin v1.0.0
```

Затем на GitHub откройте Releases → Draft a new release и выберите тег `v1.0.0`.
