#!/bin/bash

read -rp "Bot token: " bot_token
read -rp "Instagram login: " inst_login
read -rp "Instagram password: " inst_password

echo "BOT_TOKEN = '$bot_token'\nINST_LOGIN = '$inst_login'\nINST_PASSWORD = '$inst_password'" > .env

python3 -m venv bot-env
source bot-env/bin/activate

pip install -r requirements.txt
