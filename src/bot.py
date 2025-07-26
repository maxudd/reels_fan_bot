from telebot import TeleBot
import instaloader
import re
import os
from dotenv import load_dotenv, dotenv_values
import yt_dlp


# Счетчики для статистики
REELS_CNT = 0
SHORTS_CNT = 0
ERR_CNT = 0

# Настройки для yt-dlp
ydl_opts = {
    'format': 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4][height<=1080]',    # разрешение
    'outtmpl': '%(title)s.%(ext)s',     # Шаблон имени файла
    'merge_output_format': 'mp4',   # Формат выходного файла
    'noplaylist': True,             # Не загружать плейлисты
}

# Загрузка переменных окружения из .env файла
load_dotenv()
values = dotenv_values()
bot = TeleBot(values['BOT_TOKEN'])

L = instaloader.Instaloader()
L.login(values['INST_LOGIN'], values['INST_PASSWORD'])

target_inst_dir = 'reels'
if not os.path.exists(target_inst_dir):
    os.makedirs(target_inst_dir)

inst_url = 'https://www.instagram.com/reel/'
youtube_full_url = 'https://www.youtube.com/shorts/'
youtube_mobile_url = 'https://youtube.com/shorts/'


@bot.message_handler(func=lambda message: message.text.startswith(inst_url))
def download_and_send_inst(message):
    global REELS_CNT, ERR_CNT
    chat_id = message.chat.id
    text = message.text
    message_id = message.message_id
    thread_id = message.message_thread_id
    if (sender := message.forward_from):
        username = sender.username
    else:
        username = message.from_user.username
    bot.delete_message(chat_id, message_id)
    bot_message = bot.send_message(chat_id=chat_id,
                                   message_thread_id=thread_id,
                                   text='ща будет рилс...')
    matched = re.match(fr'{inst_url}(.*)/\S* ?(\S*)', text)
    if not matched:
        bot.edit_message_text(chat_id=chat_id,
                              message_id=bot_message.message_id,
                              text="ты кого наебать пытаешься?")
    else:
        shortcode = matched.group(1)
        user_caption = f'рилс от @{username}'
        text_caption = matched.group(2)
        caption = text_caption + '\n' + user_caption if text_caption else user_caption
        try:
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            L.download_post(post, target=target_inst_dir)
            for file in os.listdir(target_inst_dir):
                if file.endswith('.mp4'):
                    bot.send_video(chat_id=chat_id,
                                   message_thread_id=thread_id,
                                   video=open(f'{target_inst_dir}/{file}', 'rb'),
                                   caption=caption)
                    bot.delete_message(chat_id, bot_message.message_id)
                    REELS_CNT += 1
                os.remove(f'{target_inst_dir}/{file}')
        except instaloader.exceptions.InstaloaderException as e:
            ERR_CNT += 1
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=bot_message.message_id,
                                  text=f'рилса не будет :(\nошибка: {e}')
        except:
            ERR_CNT += 1
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=bot_message.message_id,
                                  text='ошибка при загрузке рилса, пусть админ смотрит логи')


@bot.message_handler(func=lambda message: message.text.startswith(youtube_full_url)
                     or message.text.startswith(youtube_mobile_url))
def download_and_send_yt(message):
    global SHORTS_CNT, ERR_CNT
    chat_id = message.chat.id
    text = message.text
    message_id = message.message_id
    thread_id = message.message_thread_id
    youtube_url = youtube_full_url if youtube_full_url in text else youtube_mobile_url
    if (sender := message.forward_from):
        username = sender.username
    else:
        username = message.from_user.username
    bot.delete_message(chat_id, message_id)
    bot_message = bot.send_message(chat_id=chat_id,
                                   message_thread_id=thread_id,
                                   text='ща будет шортс...')
    matched = re.match(fr'{youtube_url}.* ?(\S*)', text)
    if not matched:
        bot.edit_message_text(chat_id=chat_id,
                              message_id=bot_message.message_id,
                              text="ты кого наебать пытаешься?")
    else:
        user_caption = f'шортс от @{username}'
        text_caption = matched.group(1)
        caption = text_caption + '\n' + user_caption if text_caption else user_caption
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Получаем информацию о видео перед скачиванием
                filename = ydl.prepare_filename(ydl.extract_info(text, download=False))
                print(f'Скачивание видео: {filename}')
                ydl.download([text])
            bot.send_video(chat_id=chat_id,
                           message_thread_id=thread_id,
                           video=open(filename, 'rb'),
                           caption=caption)
            bot.delete_message(chat_id, bot_message.message_id)
            os.remove(filename)
            SHORTS_CNT += 1
        except yt_dlp.utils.DownloadError as e:
            ERR_CNT += 1
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=bot_message.message_id,
                                  text=f'шортса не будет :(\nошибка: {e}')
        except:
            ERR_CNT += 1
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=bot_message.message_id,
                                  text='ошибка при загрузке шортса. бот занят или пусть админ смотрит логи')


@bot.message_handler(commands=['status'])
def send_status(message):
    chat_id = message.chat.id
    thread_id = message.message_thread_id
    bottext = f"🤖 Бот работает. За время работы:\n" \
              f"🤤 Количество скачанных рилсов: {REELS_CNT}\n" \
              f"🩳 Количество скачанных шортсов: {SHORTS_CNT}\n" \
              f"❌ Количество ошибок: {ERR_CNT}"
    bot.send_message(chat_id=chat_id,
                     message_thread_id=thread_id,
                     text=bottext)


@bot.message_handler(commands=['start'])
def send_status(message):
    chat_id = message.chat.id
    thread_id = message.message_thread_id
    bottext = f"🤖 Привет! Основные команды бота:\n" \
              f"🤤 /status: узнать статистику по работе бота\n"
    bot.send_message(chat_id=chat_id,
                     message_thread_id=thread_id,
                     text=bottext)


# Start polling the bot
bot.infinity_polling(timeout=10, long_polling_timeout=5)
