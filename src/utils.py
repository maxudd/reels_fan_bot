import yt_dlp
import requests


def dwld_YTThumb(info, save_path):
    try:
        # Получаем информацию о видео
        thumbnail_url = info.get('thumbnail')

        # Загружаем картинку
        response = requests.get(thumbnail_url)
        
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print("Thumbnail saved successfully.")
            return save_path
        else:
            print("Failed to retrieve thumbnail.")
    except Exception as e:
        print(f"An error occurred: {e}")
