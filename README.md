# Скачиватель коротких роликов (IG, YT) для тг

## Установка
1. Склонировать этот репозиторий
2. Подготовить виртуальное окружение и библиотеки с помощью скрипта:
    ```
    bash setup.sh
    ```
3. Войти в созданное окружение
    ```
    source bot-env/bin/activate
    ```

## Запуск
```
python3 src/bot.py
```


## Docker запуск
1. Сборка Docker-образа из корневой папки проекта.
    ```
    sudo docker build -t reels-fan-bot .
    ```
2. Запуск контейнер.
    ```
    sudo docker run --env-file .env -d reels-fan-bot
    ```
3. Проверка работы.
    ```
    sudo docker logs <container_id>
    ```
    где `containter_id` можно найти по команде ```docker ps```
4. Остановка контейнера.
    ```
    sudo docker stop <container_id>
    ```
5. Удаление контейнера и образа.
    ```
    sudo docker rm <container_id>
    sudo docker rmi reels-fan-bot
    ```


## Использование
1. Добавить бота в чат и дать ему права админа
2. Прислать ссылку на рилс или шортс в чат
3. Кайфовать (брейнротить)
