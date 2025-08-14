""" This file contains parameters and configurations for the bot """
# URLs for Instagram Reels and YouTube Shorts
IG_URL = 'https://www.instagram.com/reel/'
YT_FULL_URL = 'https://www.youtube.com/shorts/'
YT_MOBILE_URL = 'https://youtube.com/shorts/'
VK_CLIPS_URL = 'https://vk.com/clip-'
VK_VIDEO_CLIPS_URL = 'https://vkvideo.ru/clip-'


""" User-updatable parameters part """
# YouTube Shorts download options
YDL_OPTS = {
    'format': 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4][height<=1080]',    # разрешение
    'outtmpl': '%(title)s.%(ext)s',  # Шаблон имени файла
    'merge_output_format': 'mp4',    # Формат выходного файла
    'noplaylist': True,              # Не загружать плейлисты
    'quiet': True                    # Выводить меньше информации
}

# Video thumbnails option
IS_THUMBS = True
IS_SHORTS = True
IS_REELS = True
IS_VKCLIPS = True
