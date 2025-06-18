# reels_fan_bot

## Docker запуск

1. Соберите Docker-образ из корневой папки проекта.
```
docker build -t reels-fan-bot .
```

2. Запустите контейнер.
```
docker run --env-file .env -d reels-fan-bot
```

3. Проверка работы.
```
docker logs <container_id>
```
где `containter_id` можно найти по команде ```docker ps```

4. Остановка контейнера.
```
docker stop <container_id>
```

5. Удаление контейнера и образа.
```
docker rm <container_id>
docker rmi reels-fan-bot
```
