# Birthday Service

## Описание
Birthday Service — это проект Django, который предоставляет функционал для управления пользователями и подписками на уведомления о днях рождения. Этот сервис позволяет пользователям подписываться на уведомления о днях рождения других пользователей и получать электронные письма с поздравлениями.

## Функции
- Регистрация и управление пользователями: Создание, просмотр и управление пользователями.
- Подписки: Пользователи могут подписываться на уведомления о днях рождения других пользователей.
- Уведомления по электронной почте: Отправка уведомлений по электронной почте в дни рождения.
- Документация API: Автоматически генерируемая документация API с помощью Swagger.

## Стек технологий
- **Веб-фреймворк:** Django
- **База данных:** PostgreSQL
- **API:** Django REST Framework
- **Аутентификация:** JWT (djangorestframework-simplejwt)
- **Оповещения:** Электронная почта
- **Очереди задач:** Celery и Redis
- **Управление зависимостями:** Poetry
- **Докеризация:** Docker и Docker Compose
- **Тестирование:** Pytest
- **Документация API:** Swagger


## Установка

### Требования
- Docker и Docker Compose

1. **Клонируйте репозиторий и перейдите в директорию проекта:**
   ```sh
   git clone https://github.com/ChebuRashkaRF/birthday_service.git
   cd birthday_service
   ```

2. **Создайте файл *.env* в корне проекта и добавьте следующие переменные окружения:**
   - ***SECRET_KEY:*** Секретный ключ для Django. Может быть сгенерирован командой python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'.
   - ***DEBUG:*** Включение режима отладки (True для разработки, False для продакшена).
   - ***ALLOWED_HOSTS:*** Список хостов, которым разрешено взаимодействие с сервером, через запятую (например, 127.0.0.1,localhost).
   - ***POSTGRES_NAME:*** Имя базы данных PostgreSQL.
   - ***POSTGRES_USER:*** Имя пользователя базы данных.
   - ***POSTGRES_PASSWORD:*** Пароль пользователя базы данных.
   - ***POSTGRES_HOST:*** Хост базы данных (например, localhost).
   - ***POSTGRES_PORT:*** Порт базы данных (обычно 5432).
   - ***EMAIL_HOST:*** Хост SMTP-сервера для отправки электронной почты (например, smtp.gmail.com для Gmail).
   - ***EMAIL_PORT:*** Порт SMTP-сервера (например, 587).
   - ***EMAIL_USE_TLS:*** Включение TLS (True для Gmail).
   - ***EMAIL_HOST_USER:*** Электронная почта отправителя.
   - ***EMAIL_HOST_PASSWORD:*** Пароль или пароль приложения для почты отправителя.   


   Пример *.env* файла:
   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   POSTGRES_NAME=postgres
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

3. **Запустите сервис с использованием Docker Compose:**
   ```sh
   docker-compose up --build
   ```
   Docker Compose автоматически создаст и настроит все необходимые сервисы, выполнит миграции базы данных и запустит сервер.


## Документация API:

   - Swagger UI: http://localhost:8000/swagger/
   - ReDoc: http://localhost:8000/redoc/


## Тестирование
   Для запуска тестов используйте команду:
   ```sh
   pytest
   ```