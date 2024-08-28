
# API "Заметки"

API приложение, построенное на фреймворке FastAPI c использованием Postgresql. Выполнено в качестве тестового задания.
Задача: спроектировать и реализовать на Python сервис, предоставляющий REST API интерфейс с методами добавления заметок, вывода списка заметок.
Требования:
- Данные необходимо хранить либо в текстовом файле, либо в базе данных
- При сохранении заметок необходимо валидировать офрграфические ошибки при помощи сервиса Яндекс.Спеллер
- Реализовать аутентификацию и авторизацию, пользователи должны иметь доступ только к своим заметкам

## Основные инструменты

- Python
- [FastApi](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://docs.docker.com/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)




## Установка

Клонировать git репозиторий:
```
git clone https://github.com/GrigoriyKuzevanov/notes-test.git
```
Перейти в директорию проекта и запустить docker-compose:
```
cd notes-test/
docker-compose up -d
```



    
## Доступный функционал и примеры использования
Проект состоит из 2-х docker контейнеров: контейнер проекта слушает порт 8081, контейнер с базой данных слушает порт 5431
```
  api:
    ports:
      - 8081:8000

  postgres:
    ports:
      - 5431:5432
```
В директории проекта находится доступный для импорта файл Postman коллекции **Notes api.postman_collection.json**

API предоставляет следующие возможности:
- **Создание пользователя: post запрос **Create User****
При создании пользователя используются два поля: username, password. Также в базе данных создается поле created_at с датой и временем создания записи и уникальный ключ id. Username пользователя должен быть уникальным.

Пример запроса:
```
POST {{URL}}/users
{
    "username": "test_user",
    "password": "test_password"
}
```
Пользователь успешно создан:
```
Status: 201 Created
{
    "username": "test_user",
    "id": 1,
    "created_at": "2024-08-28T05:49:42.709827Z"
}
```
Пользователь с переданным username уже существует:
```
Status: 422 Unprocessable Entity
{
    "detail": "User with username: test_user already exists"
}
```
- **Получение данных пользователя: get запрос **Get User****
Получить данные пользователя можно, отправив get запрос по адресу /users/{user_id}, где user_id - id запрашиваемого пользователя

Пример запроса:
```
GET {{URL}}/users/1
```
Ответ:
```
Status: 200 OK
{
    "username": "test_user",
    "id": 1,
    "created_at": "2024-08-28T05:49:42.709827Z"
}
```
Пользователя с переданным id не существует:
```
Status: 404 Not Found
{
    "detail": "User with id: 2 does not exist"
}
```
- **Авторизация пользователя: post запрос **Login****
При отправлении валидных данных формы авторизации, сервер в ответ присылает token, который используется для доступа к api заметок. Срок жизни токена доступа 60 минут по умолчанию, хранится в переменной окружения ACCESS_TOKEN_EXPIRE_MINUTES

docker-compose.yml
```
  api:
    environment:
      - ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Пример запроса:
```
POST {{URL}}/login
Content-Type: multipart/form-data

username: test_user
password: test_password
```
Успешная авторизация:
```
Status: 200 OK
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3MjQ4Mjg1Nzh9.Akb6M-gwLRkemw6JiAvbOBrvCIt_kJEX8O00FJOEMTY",
    "token_type": "bearer"
}
```
Неверный username или password:
```
Status: 403 Forbidden
{
    "detail": "invalid credentials"
}
```

Авторизованный пользователь получает доступ к операциям с заметкам, в случае неавторизованного доступа к запросам Note, пользователь получит ответ:
```
Status: 403 Forbidden
{
    "detail": "Not authorized to perform requested action"
}
```


- **Создание заметки: post запрос **Create Note****
Заметка состоит из заголовка (поле "title") и содержания заметки (поле "content"). При добавлении заметки сервер проверяет содержимое поля "content" с помощью сервиса Яндекс.Спеллер. В случае отсутсвия ошибок, заметка добавляется в базу данных. В случае наличия ошибок сервер возвращает значения слов, в которых допущены ошибки и возможные варианты исправления. Настройка языков проверки и URL сервиса доступны в переменных окружения SPELLER_URL и LANGUAGES

docker-compose.yml
```
  api:
    environment:
      - SPELLER_URL=https://speller.yandex.net/services/spellservice.json/checkText
      - LANGUAGES=ru,en
```

Пример запроса:
```
POST {{URL}}/notes
{
	"title": "test title",
    "content": "test content"
}
```
Заметка успешно создана:
```
Status: 201 Created
{
    "title": "test title",
    "content": "test content",
    "id": 1,
    "created_at": "2024-08-28T06:11:47.657081Z",
    "owner": {
        "username": "test_user",
        "id": 1,
        "created_at": "2024-08-28T05:49:42.709827Z"
    }
}
```
Заметка содержит орфографические ошибки в поле content:
```
Status: 422 Unprocessable Entity
{
    "detail": "errors in content: [{'tUst': ['trust', 'test', 'tUst', 'tyst']}, {'cAntent': ['content']}]"
}
```
Сервис Яндекс.Спеллер недоступен:
```
Status: 503 Service Unavailable
{
    "detail": "Yandex Speller sevice is not available"
}
```

- **Получение заметок: get запрос **Get Notes****
Пользователm может получить список своих заметок с помщью простого Get запроса

Пример запроса:
```
GET {{URL}}/notes
```
Ответ:
```
Status: 200 OK
[
    {
        "title": "test title",
        "content": "test content",
        "id": 1,
        "created_at": "2024-08-28T06:11:47.657081Z",
        "owner": {
            "username": "test_user",
            "id": 1,
            "created_at": "2024-08-28T05:49:42.709827Z"
        }
    }
]
```
- **Обновление заметки: put запрос **Update Notes****
Пользователь может обновить существующую заметку, отправив put запрос по адресу /notes/{note_id}, где note_id - id требуемой заметки. При этом необходимо в теле запроса, необходимо передать оба поля: title и content, которые заменят соответстующие поля заметки в базе данных с id = note_id

Пример запроса:
```
PUT {{URL}}/notes/1
{
	"title": "update title",
    "content": "some fun content"
}
```
Заметка успешно обновлена:
```
Status: 200 OK
{
    "title": "update title",
    "content": "some fun content",
    "id": 1,
    "created_at": "2024-08-28T06:11:47.657081Z",
    "owner": {
        "username": "test_user",
        "id": 1,
        "created_at": "2024-08-28T05:49:42.709827Z"
    }
}
```
Заметки с переданным id не существует:
```
{
    "detail": "Note with id: 2 does not exists"
}
```
- **Удаление заметки: delete запрос **Delete Note****
Пользователь может удалить существующую заметку, отправив delete запрос по адресу /notes/{note_id},где note_id - id требуемой заметки

Пример запроса:
```
DELETE {{URL}}/notes/1
```
Заметка успешно удалена:
```
Status: 204 No Content
```
Заметки с переданным id не существует:
```
{
    "detail": "Note with id: 2 does not exists"
}
```
