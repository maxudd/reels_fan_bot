import yt_dlp
import requests
from PIL import Image
from io import BytesIO


def crop_to_vertical(image_bytes, save_path, aspect_ratio=(9, 16)):
    image = Image.open(BytesIO(image_bytes))
    width, height = image.size
    target_ratio = aspect_ratio[0] / aspect_ratio[1]
    new_height = height
    new_width = int(new_height * target_ratio)

    if new_width > width:
        new_width = width
        new_height = int(new_width / target_ratio)

    left = (width - new_width) // 2
    top = (height - new_height) // 2
    right = left + new_width
    bottom = top + new_height

    cropped = image.crop((left, top, right, bottom))
    cropped.save(save_path)
    print(f"Thumbnail cropped to {aspect_ratio=}")
    return save_path


def dwld_YTThumb(info, save_path):
    try:
        # Получаем информацию о видео
        thumbnail_url = info.get('thumbnail', [])

        # Загружаем картинку
        response = requests.get(thumbnail_url)

        if response.status_code == 200:
            print("Thumbnail downloaded successfully.")
            crop_to_vertical(response.content, save_path)
            return save_path
            print("Failed to retrieve thumbnail.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Пример использования функции
    text = "https://youtube.com/shorts/YWkYaM3Wd6c?si=plN-okCoEXbbk4eR"
    with yt_dlp.YoutubeDL(__import__("params").YDL_OPTS) as ydl:
        info = ydl.extract_info(text, download=False)

    dwld_YTThumb(info, 'thumbnail.jpg')
