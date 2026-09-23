"""Разбор файла-ключа с координатами пикселей.

Файл ключа содержит по одной паре координат "(x, y)" на строку,
например:
    (188, 377)
    (110, 140)

Порядок координат: x - столбец (по горизонтали), y - строка
(по вертикали), то есть pixel = image.getpixel((x, y)).
"""

import re

# Пара неотрицательных целых чисел в скобках через запятую.
COORD_PATTERN = re.compile(r"\(\s*(\d+)\s*,\s*(\d+)\s*\)")


def parse_keys(path):
    """Считывает файл ключа и возвращает список координат [(x, y), ...].

    Пустые строки и посторонний текст в файле игнорируются - в файл
    попадает всё, что удалось найти регулярным выражением.
    """
    with open(path, "r", encoding="utf-8") as key_file:
        content = key_file.read()

    matches = COORD_PATTERN.findall(content)
    return [(int(x), int(y)) for x, y in matches]


def save_keys(path, coords):
    """Сохраняет список координат в файл ключа в том же формате."""
    with open(path, "w", encoding="utf-8") as key_file:
        for x, y in coords:
            key_file.write(f"({x}, {y})\n")
