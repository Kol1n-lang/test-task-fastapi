# FastAPI Test Task Project

## 🚀 Технологический стек

- **FastAPI** - современный, быстрый веб-фреймворк для построения API
- **Python 3.11** - язык программирования
- **Docker** - контейнеризация приложения
- **Redis** - кэширование и брокер сообщений
- **SQLAlchemy + PostgreSQL** - работа с базой данных
- **Pip** - менеджер пакетов Python
- **Alembic** - система миграций базы данных
- **Dishka** - DI-контейнер для управления зависимостями
- **JWT Auth** - Авторизация с помощью JWT - токенов

## 🏗️ Архитектура

Проект использует современные подходы к построению приложений, также планируется оптимизация некоторых моментов в архитектуре
### Dependency Injection (Dishka)
- Четкое разделение зависимостей
- Упрощенное тестирование компонентов
- Гибкая конфигурация сервисов

### Многослойная архитектура:
1. **API слой** (FastAPI роутеры)
2. **Сервисный слой** (бизнес-логика)
3. **Репозиторный слой** (работа с БД)
4. **Инфраструктура** (Redis, внешние API)

## ⚙️ Установка и запуск

### Способ 1: Локальный запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Kol1n-lang/fastapi-test-task.git
cd fastapi-test-task
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Настройте окружение:
- Скопируйте `.env.example` в `.env`
- Отредактируйте параметры подключения к БД и Redis
- Обновите `sqlalchemy.url` в `alembic.ini`

4. Запустите миграции:
```bash
alembic upgrade head
```

5. Запустите сервер:
```bash
uvicorn app.main:init_app --host 0.0.0.0 --port 8000 --reload
```

### Способ 2: Запуск через Docker

1. Установите Docker Desktop

2. Настройте окружение:
- Скопируйте `.env.example` в `.env`
- Замените `localhost` на имена сервисов (`db` для БД, `redis` для Redis)

3. Запустите контейнеры:
```bash
docker-compose up -d --build
```

4. Выполните миграции:
```bash
docker-compose exec app alembic upgrade head
```

5. Приложение будет доступно по адресу:
```
http://localhost:8000
```

## 🌐 Доступные эндпоинты

- `POST /api/v1/auth/register` - регистрация пользователя
- `POST /api/v1/auth/login` - авторизация получение JWT
- `POST /api/v1/bank/create-bill` - создание счета
- `GET /api/v1/bank/get-bills` - список счетов пользователя
- `GET /api/v1/bank/get-bills/{bill_id}` - получить данные счета
- `GET /api/v1/bank/get-currencies` - получить курс EUR, USD, данные кэшированы обновление установите сами
- `POST /api/v1/bankpayment` - имитация оплаты в зависимости от знака числа будет вычет или пополнение(Плохая практика использовать float, планируется изменение на  int:int)

## 📊 Примеры запросов

Регистрация пользователя:
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "securepassword"}'
```

## 🛠️ Разработка

Для работы с кодом рекомендуется:

1. Установить pre-commit хуки:
```bash
pre-commit install
```

2. Использовать форматтер (black):
```bash
black .
```

3. Проверять типы (mypy):
```bash
mypy .
```

## 📚 Документация

После запуска приложения доступны:

- Swagger UI: `http://localhost:8000/docs`

## 🤝 Участие в проекте

PR и issues приветствуются! Перед внесением изменений:

1. Создайте новую ветку
2. Добавьте тесты для нового функционала
3. Обновите документацию
4. Создайте Pull Request
