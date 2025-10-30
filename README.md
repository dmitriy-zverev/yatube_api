# YaTube API

REST API для социальной сети YaTube - платформы для публикации постов, организации их в группы и комментирования.

## Описание проекта

YaTube API предоставляет программный интерфейс для взаимодействия с социальной сетью YaTube. API позволяет:
- Создавать, просматривать, редактировать и удалять посты
- Просматривать группы постов
- Добавлять и просматривать комментарии к постам
- Управлять доступом через токен-аутентификацию

## Технологии

- Python 3.7+
- Django 3.2+
- Django REST Framework 3.12+
- drf-nested-routers
- Pillow 9.3.0

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/dmitriy-zverev/yatube_api
cd yatube_api
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Выполните миграции:
```bash
cd yatube_api
python manage.py migrate
```

5. Создайте суперпользователя (опционально):
```bash
python manage.py createsuperuser
```

6. Запустите сервер разработки:
```bash
python manage.py runserver
```

7. Проверьте, что сервер проходит все тесты:
```bash
pytest tests
```

API будет доступен по адресу: `http://127.0.0.1:8000/api/v1/`

## Аутентификация

API использует Token Authentication. Для получения токена отправьте POST-запрос:

```bash
POST /api/v1/api-token-auth/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

Ответ:
```json
{
    "token": "your_auth_token"
}
```

Используйте токен в заголовке Authorization для авторизованных запросов:
```
Authorization: Token your_auth_token
```

## API эндпоинты

### Посты (только для авторизованных пользователей)

#### Получить список всех постов
```
GET /api/v1/posts/
```

#### Создать пост
```
POST /api/v1/posts/
Content-Type: application/json
Authorization: Token your_auth_token

{
    "text": "Текст поста",
    "group": 1  # ID группы (опционально)
}
```

#### Получить пост по ID
```
GET /api/v1/posts/{post_id}/
```

#### Обновить пост (только автор)
```
PUT /api/v1/posts/{post_id}/
Content-Type: application/json
Authorization: Token your_auth_token

{
    "text": "Обновленный текст поста",
    "group": 2
}
```

#### Частично обновить пост (только автор)
```
PATCH /api/v1/posts/{post_id}/
Content-Type: application/json
Authorization: Token your_auth_token

{
    "text": "Новый текст"
}
```

#### Удалить пост (только автор)
```
DELETE /api/v1/posts/{post_id}/
Authorization: Token your_auth_token
```

### Группы (только для авторизованных пользователей и только для просмотра групп)

#### Получить список всех групп
```
GET /api/v1/groups/
```

#### Получить группу по ID
```
GET /api/v1/groups/{group_id}/
```

### Комментарии (только для авторизованных пользователей)

#### Получить все комментарии к посту
```
GET /api/v1/posts/{post_id}/comments/
```

#### Добавить комментарий к посту
```
POST /api/v1/posts/{post_id}/comments/
Content-Type: application/json
Authorization: Token your_auth_token

{
    "text": "Текст комментария"
}
```

#### Получить комментарий по ID
```
GET /api/v1/posts/{post_id}/comments/{comment_id}/
```

#### Обновить комментарий (только автор)
```
PUT /api/v1/posts/{post_id}/comments/{comment_id}/
Content-Type: application/json
Authorization: Token your_auth_token

{
    "text": "Обновленный текст комментария"
}
```

#### Частично обновить комментарий (только автор)
```
PATCH /api/v1/posts/{post_id}/comments/{comment_id}/
Content-Type: application/json
Authorization: Token your_auth_token

{
    "text": "Новый текст"
}
```

#### Удалить комментарий (только автор)
```
DELETE /api/v1/posts/{post_id}/comments/{comment_id}/
Authorization: Token your_auth_token
```

## Примеры запросов

### Получение списка постов с помощью curl
```bash
curl http://127.0.0.1:8000/api/v1/posts/ \
  -H "Authorization: Token your_auth_token"
```

### Создание поста с помощью curl
```bash
curl -X POST http://127.0.0.1:8000/api/v1/posts/ \
  -H "Authorization: Token your_auth_token" \
  -H "Content-Type: application/json" \
  -d '{"text": "Мой новый пост"}'
```

### Добавление комментария с помощью Python requests
```python
import requests

url = "http://127.0.0.1:8000/api/v1/posts/1/comments/"
headers = {
    "Authorization": "Token your_auth_token",
    "Content-Type": "application/json"
}
data = {
    "text": "Отличный пост!"
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

## Permissions (Разрешения)

- **Посты**: 
  - Просмотр - только авторизованным пользователям
  - Создание - только авторизованным пользователям
  - Редактирование/удаление - только автору поста
  
- **Группы**: 
  - Просмотр - только авторизованным пользователям
  - Редактирование - недоступно через API
  
- **Комментарии**: 
  - Просмотр - только авторизованным пользователям
  - Создание - только авторизованным пользователям
  - Редактирование/удаление - только автору комментария

## Формат ответов

Все ответы возвращаются в формате JSON.

### Пример ответа для поста:
```json
{
    "id": 1,
    "text": "Текст поста",
    "pub_date": "2025-10-30T11:30:00.000000Z",
    "author": "username",
    "image": null,
    "group": 1
}
```

### Пример ответа для комментария:
```json
{
    "id": 1,
    "author": "username",
    "post": 1,
    "text": "Текст комментария",
    "created": "30.10.2025 14:30:00"
}
```

### Пример ответа для группы:
```json
{
    "id": 1,
    "title": "Название группы",
    "slug": "group-slug",
    "description": "Описание группы"
}
```

## Тестирование

Проект включает набор тестов. Для их запуска выполните:
```bash
pytest tests
```

## Postman Collection

Проект включает Postman Collection для тестирования API. Для этого загрузите файл CRUD.postman_collection.json и подключите его к Postman.

## Документация API

После запуска сервера автоматическая документация API доступна по адресу:
- Browsable API: `http://127.0.0.1:8000/api/v1/`

## Структура проекта

```
yatube_api/
├── yatube_api/
│   ├── api/              # API приложение
│   │   ├── permissions.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── posts/            # Приложение с моделями
│   │   ├── models.py
│   │   ├── serializers.py
│   │   └── views.py
│   ├── yatube_api/       # Настройки проекта
│   │   ├── settings.py
│   │   └── urls.py
│   └── manage.py
├── tests/                # Тесты
├── requirements.txt      # Зависимости
└── README.md            # Документация
```

## Автор

YaTube API - учебный проект курса Python-разработчик

## Лицензия

Этот проект создан в образовательных целях.
