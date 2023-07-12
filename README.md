# Testhub - сервис для прохождения тестирований

### Инструкция по установке
- Клонировать репозиторий
```
git clone https://github.com/firepanda70/testhub
```
- Добавить в диреторию ```infra/``` файл ```.env``` и заполнить переменными. Пример данных в файле ```.env.example```
- Поднять контейнеры через docker-compose в той же директории
```
docker compose up -d
```
- Открыть консоль контейнера ```testhub-app-1```
- Внутри контейнера
  1. Выполнить миграции
  2. Загрузить данные в БД из файла dump.json
  3. Загрузить статику (На предупреждение ответить ```yes``` )
```
python manage.py migrate
python manage.py loaddata dump.json
python manage.py collectstatic
```
- Profit!

Сервер будет доступен на [localhost](http://localhost/)<br>
Админка [тут](http://localhost/admin/)<br>
Данные админки:
```
login: admin
pass: admin
```

### Технологии
- django
- Docker
- gunicorn
- dotenv
