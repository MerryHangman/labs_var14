"""Кодирование и декодирование текста в изображении.

Задание 1.2 (вариант 14): метод b1-R, b0-R - используются 0-й и 1-й
биты байта, отвечающего за красный цвет. В эти 2 бита одного пикселя
помещается 2 бита сообщения, поэтому один символ (1 байт = 8 бит)
занимает ровно 4 пикселя.
"""

import random

from PIL import Image

RED_CHANNEL_INDEX = 0
BITS_PER_PIXEL = 2
PIXELS_PER_CHAR = 8 // BITS_PER_PIXEL  # 4 пикселя на символ
LOW_BITS_MASK = 0b11111100  # обнуляет 2 младших бита красного канала

TEXT_ENCODING = "cp1251"


def capacity_in_chars(width, height):
    """Сколько символов сообщения помещается в изображение."""
    total_pixels = width * height
    return total_pixels // PIXELS_PER_CHAR


def generate_key(width, height, char_count, seed=None):
    """Генерирует список уникальных случайных координат пикселей.

    На каждый символ сообщения выделяется PIXELS_PER_CHAR пикселей.
    """
    pixels_needed = char_count * PIXELS_PER_CHAR
    total_pixels = width * height
    if pixels_needed > total_pixels:
        raise ValueError(
            f"Сообщение из {char_count} символов требует "
            f"{pixels_needed} пикселей, а в изображении их "
            f"только {total_pixels}."
        )

    rng = random.Random(seed)
    all_positions = [(x, y) for x in range(width) for y in range(height)]
    chosen = rng.sample(all_positions, pixels_needed)
    return chosen


def _char_to_bit_groups(char_byte):
    """Разбивает 1 байт символа на 4 группы по 2 бита."""
    bits = format(char_byte, "08b")
    return [int(bits[i:i + BITS_PER_PIXEL], 2) for i in range(0, 8, 2)]


def _bit_groups_to_char(groups):
    """Собирает 1 байт символа из 4 групп по 2 бита."""
    bits = "".join(format(group, "02b") for group in groups)
    return int(bits, 2)


def encode_message(image, message, coords, verbose_first_char=True):
    """Кодирует сообщение в копию изображения методом b1-R, b0-R.

    Возвращает новое изображение (исходное не изменяется) и,
    для первого символа, отладочную информацию: биты символа,
    исходные и изменённые значения пикселей.
    """
    encoded_image = image.copy()
    message_bytes = message.encode(TEXT_ENCODING)

    debug_info = None

    for char_index, char_byte in enumerate(message_bytes):
        bit_groups = _char_to_bit_groups(char_byte)
        pixel_slice = coords[
            char_index * PIXELS_PER_CHAR: (char_index + 1) * PIXELS_PER_CHAR
        ]

        originals = []
        modified = []
        for (x, y), group in zip(pixel_slice, bit_groups):
            pixel = list(encoded_image.getpixel((x, y)))
            originals.append(tuple(pixel))

            red = pixel[RED_CHANNEL_INDEX]
            new_red = (red & LOW_BITS_MASK) | group
            pixel[RED_CHANNEL_INDEX] = new_red
            encoded_image.putpixel((x, y), tuple(pixel))
            modified.append(tuple(pixel))

        if char_index == 0 and verbose_first_char:
            debug_info = {
                "char": message[0],
                "bits": format(char_byte, "08b"),
                "originals": originals,
                "modified": modified,
            }

    return encoded_image, debug_info


def decode_message(image, coords, char_count):
    """Декодирует char_count символов из изображения по списку координат."""
    result_bytes = bytearray()

    for char_index in range(char_count):
        pixel_slice = coords[
            char_index * PIXELS_PER_CHAR: (char_index + 1) * PIXELS_PER_CHAR
        ]
        groups = []
        for x, y in pixel_slice:
            red = image.getpixel((x, y))[RED_CHANNEL_INDEX]
            groups.append(red & 0b11)
        result_bytes.append(_bit_groups_to_char(groups))

    return bytes(result_bytes).decode(TEXT_ENCODING, errors="replace")


def load_image(path):
    """Открывает изображение и приводит его к RGB."""
    return Image.open(path).convert("RGB")
