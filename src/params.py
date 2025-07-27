# Настройки для yt-dlp
YDL_OPTS = {
    'format': 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4][height<=1080]',    # разрешение
    'outtmpl': '%(title)s.%(ext)s',     # Шаблон имени файла
    'merge_output_format': 'mp4',   # Формат выходного файла
    'noplaylist': True,             # Не загружать плейлисты
}
