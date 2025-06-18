from telebot import TeleBot
import instaloader
import re
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()
values = dotenv_values()
bot = TeleBot(values['BOT_TOKEN'])

L = instaloader.Instaloader()
L.login(values['INST_LOGIN'], values['INST_PASSWORD'])
target_directory = 'reels'

@bot.message_handler(func=lambda message: message.text.startswith('https://www.instagram.com/reel/'))
def download_and_send(message):
    chat_id = message.chat.id
    text = message.text
    message_id = message.message_id
    thread_id = message.message_thread_id
    if (sender:=message.forward_from):
        username = sender.username
    else:
        username = message.from_user.username 
    bot.delete_message(chat_id, message_id)
    bot_message = bot.send_message(chat_id=chat_id,
                                   message_thread_id=thread_id,
                                   text='ща будет рилс...')
    matched = re.match(r'https://www.instagram.com/reel/(.*)/.*', text)
    if not matched:
        bot.edit_message_text(chat_id=chat_id,
                              message_id=bot_message.message_id,
                              text=f'ты кого наебать пытаешься?')
    else:
        shortcode = matched.group(1)
        try:
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            L.download_post(post, target=target_directory)
            for file in os.listdir(target_directory):
                if file.endswith('.mp4'):
                    # bot.edit_message_media(chat_id=chat_id, message_id=bot_message.message_id, media=open(f'reels/{file}', 'rb'))
                    bot.send_video(chat_id=chat_id,
                                message_thread_id=thread_id,
                                video=open(f'{target_directory}/{file}', 'rb'),
                                caption=f'рилс от @{username}')
                    # bot.edit_message_text(chat_id=chat_id, message_id=bot_message.message_id, text='')
                    bot.delete_message(chat_id, bot_message.message_id)
                os.remove(f'reels/{file}')
        except instaloader.exceptions.InstaloaderException as e:
            bot.edit_message_text(chat_id=chat_id,
                                message_id=bot_message.message_id,
                                text=f'рилса не будет :(\nошибка: {e}')

bot.polling()