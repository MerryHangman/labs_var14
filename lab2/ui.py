"""Консольный ввод данных для лабы 2 с проверкой регулярными выражениями."""

import os
import re

# Путь к wav-файлу по умолчанию (вариант 14).
DEFAULT_WAV_PATH = os.path.join(
    os.path.dirname(__file__), "data", "14.wav"
)

# Разрешаем путь из букв, цифр, пробелов, точек, слэшей, дефисов,
# подчёркиваний и кириллицы - на случай "C:/Users/Имя/14.wav".
WAV_PATH_PATTERN = re.compile(r"^[\w\s./:\\\-А-Яа-яЁё]+\.wav$", re.IGNORECASE)

# Только неотрицательное целое число.
POSITIVE_INT_PATTERN = re.compile(r"^\d+$")


def read_line(prompt):
    """Безопасный ввод строки. Возвращает None при Ctrl+C / Ctrl+D."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def ask_wav_path():
    """Запрашивает путь к wav-файлу, проверяя его регулярным выражением.

    Пустой ввод принимает путь по умолчанию (файл варианта 14).
    """
    while True:
        raw = read_line(
            f"Путь к wav-файлу (Enter - файл по умолчанию "
            f"'{DEFAULT_WAV_PATH}'): "
        )
        if raw is None:
            return None

        path = raw.strip()
        if path == "":
            return DEFAULT_WAV_PATH

        if not WAV_PATH_PATTERN.match(path):
            print("Путь должен указывать на файл с расширением .wav\n")
            continue

        if not os.path.isfile(path):
            print(f"Файл '{path}' не найден. Проверьте путь.\n")
            continue

        return path


def ask_sample_count(max_value):
    """Запрашивает количество отсчётов для графика чтения сигнала.

    Проверяет ввод регулярным выражением (только цифры). Если введено
    число больше длины сигнала, оно обрезается до max_value, чтобы
    программа не падала на некорректном вводе.
    """
    while True:
        raw = read_line(
            f"Введите количество отсчётов для графика "
            f"(1 - {max_value}): "
        )
        if raw is None:
            return None

        raw = raw.strip()
        if not POSITIVE_INT_PATTERN.match(raw):
            print("Нужно ввести целое неотрицательное число.\n")
            continue

        count = int(raw)
        if count == 0:
            print("Количество отсчётов должно быть больше нуля.\n")
            continue

        if count > max_value:
            print(
                f"В файле всего {max_value} отсчётов, "
                f"будут показаны все.\n"
            )
            count = max_value

        return count
