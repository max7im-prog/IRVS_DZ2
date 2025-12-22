# ДЗ 2: Weather Logger

В этом репозитории представлен контейнер Flask-приложения, который:

* получает данные о погоде с публичного API
* сохраняет их в базе данных PostgreSQL

## Сборка и запуск контейнеров

```bash
cd ./app
docker-compose up --build
```

## Проверка работы

### Запрос текущей погоды

```bash
curl -X POST http://localhost:5000/log
```

### Запрос истории

```bash
curl http://localhost:5000/history
```
