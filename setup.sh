#!/bin/bash

read -rp "Bot token: " bot_token
read -rp "Instagram login: " inst_login
read -rp "Instagram password: " inst_password

cat > .env <<EOF
BOT_TOKEN='$bot_token'
INST_LOGIN='$inst_login'
INST_PASSWORD='$inst_password'
EOF

python3 -m venv bot-env
source bot-env/bin/activate

pip install -r requirements.txt
