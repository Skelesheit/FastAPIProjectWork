# FastAPI Project

Это серверное приложение на FastAPI, построенное по принципам DDD (Domain-Driven Design). Поддерживается запуск через Poetry, Docker или Docker Compose. Используется PostgreSQL, Alembic, Pydantic и асинхронный стек Python.

---

## 📦 Технологии

- **Python 3.12**
- **FastAPI** — современный асинхронный веб-фреймворк
- **Uvicorn** — ASGI-сервер
- **SQLAlchemy 2.x** — ORM
- **AsyncPG** — драйвер PostgreSQL
- **Alembic** — миграции
- **Poetry** — менеджер зависимостей
- **Docker / Docker Compose** — деплой и автоматическое развёртывание
- **Pydantic / Pydantic Settings** — сериализатор
- **bcrypt / JWT / Email подтверждение**
- **Celery** - worker для отправки писем
- **pytest** - тестирование API

---

## 📑 Оглавление

- [📖 Введение](#-введение)
- [🛠 Технологии](#-технологии)
- [📂 Структура проекта](#-структура-проекта)
- [⚙️ Установка и запуск](#️-установка-и-запуск)
  - [🚀 Запуск](#-запуск)
- [🔑 Аутентификация и авторизация](#-аутентификация-и-авторизация)
- [📬 Celery и фоновые задачи](#-celery-и-фоновые-задачи)
- [🗃 База данных](#-база-данных)
- [📜 Логирование](#-логирование)
- [🧪 Тестирование](#-тестирование)
- [📌 Навигация по слоям](#-навигация-по-слоям)
  - [🔑 Auth](#-auth)
  - [🗃 DB](#-db)
  - [📡 Handlers](#-handlers)
  - [📦 Serializers](#-serializers)
  - [⚙️ Services](#-services)
  - [📚 Use Cases](#-use-cases)
  - [📜 Logging](#-logging)
  - [📬 Celery](#-celery)
  - [🧪 Testing](#-testing)
- [📅 Roadmap](#-roadmap)
- [🤝 Контрибьютинг](#-контрибьютинг)
- [📄 Лицензия](#-лицензия)

---

## 📌 Навигация по всему проекту

- [🔑 Auth](src/auth/docs.md)
- [📡 Clients](src/clients/docs.md)
- [🗃 DB](src/db/docs.md)
- [📡 Handlers](src/handlers/docs.md)
- [📦 Serializers](src/serializers/docs.md)
- [⚙️ Services](src/services/docs.md)
- [📜 Logging](src/logging/docs.md)
- [📬 Infrastructure (Celery/Redis)](src/infrastructure/docs.md)
- [📚 Use Cases](src/use_cases/docs.md)
- [🧪 Testing](src/tests/docs.md)

---

## 🚀 Запуск проекта

Не забудьте правильно настроить `.env` для Docker или локального развёртывания.
Например, важно, чтобы в Docker `HOST_NAME=db` а для локальной например `HOST_NAME=localhost`

### 🔹 Локально
1) Клонируйте проект
```bash
  git clone https://github.com/username/project.git
  cd project
```
2) Установить зависимости через `poetry`
```bash
  poetry install
```
или через `pip`
```bash
  pip install -r requirements.txt
```
2) Применить миграции
```bash
  alembic upgrade head
```

3) Запустить Redis (в проекте есть файл `redis-test-docker.yml`)
```bash
  docker compose -f redis-test-docker.yml up -d
# или: docker-compose -f redis-test-docker.yml up -d
```

или запустите Redis локально на вашем `linux`

4) Запустить Celery worker (очередь e-mail)
```bash
# Воркер слушает очередь "mail". Приложение Celery объявлено в src/infrastructure/celery/main.py как celery_app
  celery -A src.infrastructure.celery.main:celery_app worker -Q mail -l info
```

5) Запустить приложение
```bash
  uvicorn main:app --reload
# 
```
или через poetry:
```bash
  poetry run uvicorn main:app --reload
```

### 🔹 Через Docker

```bash
docker-compose up --build
```
---


При использовании docker-compose миграции применяются автоматически через скрипт `init_db.sh`.

---

## 🔑 Аутентификация и авторизация

- JWT токены (Access + Refresh)
- Refresh хранится в HttpOnly Cookie
- Middleware логирует `user_id` и `enterprise_id`

Примеры эндпоинтов:
- `POST /user/register` — регистрация
- `POST /user/login` — вход
- `POST /auth/refresh` — обновление токена
- `POST /auth/logout` — выход

---

## 📬 Celery и фоновые задачи

- Брокер: RabbitMQ / Redis
- Задачи: отправка почты, обработка данных и т.п.
- Запуск worker:
```bash
celery -A src.celery worker --loglevel=info
```
---

## 🧾 Логирование и перехват ошибок

### Что логируется
- **Доступ (access):** каждый запрос/ответ через `src/logging/access.py` (`access_middleware`), в ответ добавляется `X-Request-Id`.
- **Ошибки:** единый перехватчик в `src/handlers/error_handler.py` (ServiceError, ValidationError, HTTPException, IntegrityError, прочие).

### Формат логов
Логи — структурированный JSON (см. `src/logging/formatters.py`). Пример записи:
```json
{
  "level": "INFO",
  "msg": "access",
  "logger": "access",
  "time": "2025-08-15T12:00:00",
  "request_id": "1b2c-...-9f",
  "method": "GET",
  "path": "/auth/me",
  "status": 200,
  "details": { "duration_ms": 8 }
}
```

### Кастомные ошибки
- Базовый класс: `src/services/errors.py::ServiceError`
- Типовые: `ValidationFailed`, `Conflict`, `PreconditionFailed`, `ExternalServiceError`, `NotUniqueEmail`, …
- Ответы в одном формате:
```json
{
  "error": { "code": "VALIDATION_FAILED", "message": "...", "details": { /* ... */ } },
  "request_id": "1b2c-...-9f"
}
```



## 🧱 Архитектура проекта (DDD)

Проект реализован с использованием подхода **DDD (Domain-Driven Design)**. Каждая директория в папке `src/` отражает определённую область ответственности:

| Папка             | Назначение                                                                    |
|-------------------|-------------------------------------------------------------------------------|
| `auth/`           | Авторизация, валидация токенов, хеширование, middleware                       |
| `clients/`        | Взаимодействие с внешними сервисами: капча, Dadata, почта                     |
| `db/`             | Работа с базой данных: модели, сессии, enum-перечисления                      |
| `handlers/`       | FastAPI-маршруты (эндпоинты), обрабатывающие запросы                          |
| `serializers/`    | Схемы сериализации/десериализации на Pydantic                                 |
| `services/`       | Бизнес-логика (например, регистрация, логин, проверка капчи)                  |
| `use_cases/`      | Конкретные сценарии взаимодействия (workflows), завязанные на доменную логику |
| `tests/`          | Тестирование API                                                              |
| `logging/`        | Логирование API                                                               |
| `infrastructure/` | То, что находится рядом с API - инфраструктура: celery и redis                |
| `__init__.py`     | Помечает директории как модули Python                                         |

DDD помогает разделять ответственность и упрощает масштабирование проекта, особенно в микросервисной или командной архитектуре.



## 📂 Структура проекта

```
.
├── Dockerfile    # Dockerfile приложения
├── README.md
├── alembic
│   ├── env.py    # Инициализация Alembic
│   └── versions
│       └── fc8a7b8c5c1d_ñ«íáó½Ñ¡δ_¬απñδ.py    # Миграция Alembic
├── alembic.ini    # Alembic конфигурация
├── config.py    # Настройки Pydantic
├── docker-compose.yml    # Docker Compose инфраструктуры
├── init_db.sh    # Скрипт авто-миграций
├── main.py    # Точка входа (FastAPI app)
├── redis-test-docker.yml
└── src
    ├── __init__.py
    ├── auth
    │   ├── __init__.py    # Модуль аутентификации
    │   ├── dep.py    # Модуль аутентификации
    │   ├── exceptions.py    # Модуль аутентификации
    │   ├── hash.py    # Модуль аутентификации
    │   ├── middleware.py    # Модуль аутентификации
    │   └── token.py    # Модуль аутентификации
    ├── clients
    │   ├── __init__.py    # Клиент внешнего API
    │   ├── captcha.py    # Клиент внешнего API
    │   ├── dadata.py    # Клиент внешнего API
    │   ├── html.py    # Клиент внешнего API
    │   └── mail.py    # Клиент внешнего API
    ├── db
    │   ├── __init__.py    # БД: модели/сессии/enum
    │   ├── base.py    # БД: модели/сессии/enum
    │   ├── db.py    # БД: модели/сессии/enum
    │   ├── db_boundary.py    # БД: модели/сессии/enum
    │   ├── enterprise_base.py    # БД: модели/сессии/enum
    │   ├── enums.py    # БД: модели/сессии/enum
    │   ├── func.py    # БД: модели/сессии/enum
    │   ├── models    # БД: модели/сессии/enum
    │   │   ├── __init__.py
    │   │   ├── enterprise.py
    │   │   ├── machines.py
    │   │   ├── materials.py
    │   │   └── users.py
    │   └── utils    # БД: модели/сессии/enum
    │       ├── __init__.py
    │       ├── consts.py
    │       ├── orm.py
    │       └── transfer.py
    ├── handlers
    │   ├── __init__.py    # FastAPI роутеры
    │   ├── auth.py    # FastAPI роутеры
    │   ├── clients.py    # FastAPI роутеры
    │   ├── enterpise.py    # FastAPI роутеры
    │   ├── error_handler.py    # FastAPI роутеры
    │   ├── resources    # FastAPI роутеры
    │   │   ├── __init__.py
    │   │   ├── assortment.py
    │   │   ├── assortment_gost.py
    │   │   ├── assortment_type.py
    │   │   ├── gosts.py
    │   │   ├── machine_type.py
    │   │   ├── machines.py
    │   │   ├── material_categories.py
    │   │   ├── materials.py
    │   │   ├── methods.py
    │   │   ├── operation_type.py
    │   │   ├── resources.py
    │   │   ├── toolings.py
    │   │   └── tools.py
    │   └── user.py    # FastAPI роутеры
    ├── infrastructure
    │   ├── __init__.py    # Инфраструктура (Redis, Celery)
    │   ├── celery    # Инфраструктура (Redis, Celery)
    │   │   ├── __init__.py
    │   │   ├── mail.py
    │   │   └── main.py    # Точка входа (FastAPI app)
    │   └── redis    # Инфраструктура (Redis, Celery)
    │       ├── __init__.py
    │       ├── invite_token.py
    │       └── main.py    # Точка входа (FastAPI app)
    ├── logging
    │   ├── __init__.py    # Логирование
    │   ├── access.py    # Логирование
    │   ├── context.py    # Логирование
    │   ├── errors.py    # Логирование
    │   ├── formatters.py    # Логирование
    │   └── setup.py    # Логирование
    ├── serializers
    │   ├── __init__.py    # Pydantic-схемы
    │   ├── clients.py    # Pydantic-схемы
    │   ├── enterprise.py    # Pydantic-схемы
    │   ├── resources.py    # Pydantic-схемы
    │   ├── token.py    # Pydantic-схемы
    │   └── user.py    # Pydantic-схемы
    ├── services
    │   ├── __init__.py    # Бизнес-логика/сервисы
    │   ├── auth_service.py    # Бизнес-логика/сервисы
    │   ├── client_service.py    # Бизнес-логика/сервисы
    │   ├── enterprise_service.py    # Бизнес-логика/сервисы
    │   ├── errors.py    # Бизнес-логика/сервисы
    │   ├── resources    # Бизнес-логика/сервисы
    │   │   ├── __init__.py
    │   │   ├── assortment_service.py
    │   │   ├── assortment_type_service.py
    │   │   ├── gost_assortment_service.py
    │   │   ├── gosts_service.py
    │   │   ├── machine_service.py
    │   │   ├── machine_type_service.py
    │   │   ├── material_category_service.py
    │   │   ├── material_service.py
    │   │   ├── method_service.py
    │   │   ├── operation_type_service.py
    │   │   ├── tool_service.py
    │   │   └── tooling_service.py
    │   ├── translators.py    # Бизнес-логика/сервисы
    │   └── user_service.py    # Бизнес-логика/сервисы
    ├── tests
    │   ├── __init__.py    # Тесты
    │   └── conftest.py    # Тесты
    └── use_cases
        ├── __init__.py    # Workflow сценарии
        ├── fill_data_workflow.py    # Workflow сценарии
        └── join_employee_workflow.py    # Workflow сценарии
```


---

## 🧩 Use Cases

| Файл                    | Назначение                                                                              |
| ----------------------- |-----------------------------------------------------------------------------------------|
| `fill_data_workflow.py` | Логика пошагового заполнения данных пользователем (важно: используется одна транзакция) |
| `join_employee_workflow.py` | Добавление сотрудника в предприятие                           |

---

## 💾 ORM и Base-класс

Базовая модель `Base` (в `src/db/base.py`) предоставляет асинхронные методы CRUD, которые можно использовать:

* **с явной сессией**: `create_with_session`, `update_with_session`, `delete_with_session`
* **без явной сессии**: `create`, `update`, `delete` (сессия создаётся внутри метода)

Это даёт гибкость при работе как внутри транзакций, так и вне их.

---

## 🧬 Модели

| Модель               | Назначение                                                          |
| -------------------- | ------------------------------------------------------------------- |
| `User`               | Основной пользователь. Email, пароль, тип (ИП, Юр. лицо, Физ. лицо) |
| `RefreshToken`       | JWT refresh-токен пользователя, срок действия                       |
| `Contact`            | Контактные данные пользователя (город, адрес, телефон)              |
| `IndividualProfile`  | Профиль физического лица (ФИО)                                      |
| `LegalEntity`        | Юридическое лицо или ИП (ИНН, ОГРН, ФИО директора)                  |
| `LegalEntityProfile` | Доп. профиль юр. лица (наименование, ОПФ)                           |

Все модели наследуются от `Base`, имеют асинхронные методы, и связаны через `relationship`.
У Него есть стандартные методы: `get()` `create()` `update()` `delete()`
А также методы с возможностью использовать единую сессию или транзакцию:
`get_with_session` `create_with_session()` `update_with_session()` `delete_with_session()`


---

## 🧪 Эндпоинты

| Метод | Эндпоинт                | 🔒 | Описание                               |
|-------|-------------------------|----|----------------------------------------|
| POST  | `/user/register`        |    | Регистрация пользователя               |
| POST  | `/user/login`           |    | Авторизация                            |
| POST  | `/user/logout`          | 🔒 | Выход из аккаунта                      |
| POST  | `/user/fill-data`       | 🔒 | Заполнение анкеты                      |
| GET   | `/auth/me`              | 🔒 | Получение данных текущего пользователя |
| GET   | `/auth/logout`          | 🔒 | Выход из системы                       |
| GET   | `/auth/refresh`         |    | Обновление access-токена               |
| GET   | `/dadata/suggest/{inn}` |    | Поиск по ИНН                           |
| GET   | `/mail/confirm/<token>` |    | Подтверждение почты                    |
| CRUD  | `/resources/*`          | 🔒 | CRUD операции (⚠️ будут legacy)        |


---

## Подробнее

### 1. `/client/suggest/<inn>`

- **Метод**: `GET`
- **Описание**: Запрос по ИНН данных о юр. лице или ИП

### 2. `/client/mail/<token>`

- **Метод**: `GET`
- **Описание**: принимает токен для подтверждения email

### 3. `/user/register`

- **Метод**: `POST`
- **Описание**: Регистрирует нового пользователя.
- **Параметры**:
  - `email`: Электронная почта пользователя.
  - `password`: Пароль пользователя.
  - `captchaToken`: токен капчи от Яндекса
- **Пример запроса**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword",
    "captchaToken": "string"
  
  }
  ```

### 4. `/user/login`

- **Метод**: `POST`
- **Описание**: Логин пользователя.
- **Параметры**:
  - `email`: Электронная почта пользователя.
  - `password`: Пароль пользователя.
- **Пример запроса**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```
### 5. `/user/fill-data`

- **Метод**: `POST`
- **Описание**: Заполнение данных пользователя.
- **Параметры**: Зависит от модели пользователя (требуется авторизация).

### 6. `/user/logout`

- **Метод**: `GET`
- **Описание**: Выйти из аккаунта (требуется авторизация).

### 7. `/auth/me`

- **Метод**: `GET`
- **Описание**: Получить информацию о текущем пользователе (требуется авторизация).

### 8. `/auth/refresh`

- **Метод**: `GET`
- **Описание**: обновление access токена при помощи refresh (refresh под капотом тоже обновляется).

### 9 `/resources/`

- **Методы**: `CREATE`, `GET`, `PUT`, `DELETE`
- **Описание**: Типичные CRUD операции
- **Устарело**: множество ORM моделей устарели, будет переписано в новой коммите 


## Визуализация и откладка

Для тестирования эндпоинтов используется swagger UI
- **эндпоинты**: доступны по адресу /
- **авторизация по токенам**: доступна при помощи кнопки `Authorize` -
не забудьте при подстановке токена вставлять `Bearer <token>`


## 📘 Swagger UI

Доступен по адресу:
```
http://localhost:8000/docs
```
Либо:
```
http://localhost:8000/
```

Для авторизации используйте `Bearer <token>`.

---

## 🔧 Alembic миграции

### 📌 Применение:

```bash
poetry run alembic upgrade head
```

### 🛠 Создание:

```bash
poetry run alembic revision --autogenerate -m "new migration"
```

---

## 🧼 Отладка

- `.env` обязателен: настройка подключения к БД, секретов и SMTP.
- `example.env` служит примером для заполнения полей.
- `alembic.ini` должен содержать корректный `sqlalchemy.url`
- для чистого старта можно сбросить volume:

```bash
docker compose down -v
```

---

## 🧑‍💻 Автор

**Skelesheit**  
📧 skelesheit@gmail.com  

