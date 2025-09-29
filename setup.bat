@echo off
setlocal

set /p bot_token="Enter telegram-bot API: "
set /p inst_login="Enter Instagram login: "
set /p inst_password="Enter Instagram password: "

(
echo BOT_TOKEN='%bot_token%'
echo INST_LOGIN='%inst_login%'
echo INST_PASSWORD='%inst_password%'
) > .env

set /p create_venv="Create Python venv? [Y/n]: "

if /I "%create_venv%"=="Y" (
    python -m venv bot-env
    call bot-env\Scripts\activate
    pip install -r requirements.txt
)

endlocal
