"""Декодирование текста, спрятанного в синем канале пикселей.

Задание 1.1 (вариант 14): каждый байт текста записан в байт пикселя,
отвечающего за синий цвет. Координаты изменённых пикселей - в файле
keys14.txt.
"""

from PIL import Image

try:
    from lab3.key_parser import parse_keys
except ImportError:
    from key_parser import parse_keys

BLUE_CHANNEL_INDEX = 2

# Кодировка, в которой один символ текста укладывается ровно в 1 байт.
TEXT_ENCODING = "cp1251"


def decode_blue_channel(image_path, keys_path):
    """Декодирует сообщение из синего канала пикселей по файлу ключа.

    Возвращает:
        message (str) - декодированный текст;
        coords (list[tuple[int, int]]) - использованные координаты.
    """
    image = Image.open(image_path).convert("RGB")
    width, height = image.size

    coords = parse_keys(keys_path)
    if not coords:
        raise ValueError(f"В файле ключа '{keys_path}' не найдено координат")

    raw_bytes = bytearray()
    for x, y in coords:
        if not (0 <= x < width and 0 <= y < height):
            raise ValueError(
                f"Координата ({x}, {y}) выходит за границы "
                f"изображения {width}x{height}"
            )
        pixel = image.getpixel((x, y))
        raw_bytes.append(pixel[BLUE_CHANNEL_INDEX])

    # errors="replace" не даёт программе упасть, если байт не входит
    # в таблицу cp1251 (например, ключ оказался не тем).
    message = bytes(raw_bytes).decode(TEXT_ENCODING, errors="replace")

    return message, coords
