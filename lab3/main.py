"""Лабораторная работа №3. Вариант 14. Стеганография.

Задание 1.1: декодирование сообщения из синего канала пикселей
             (new14.png + keys14.txt).
Задание 1.2: кодирование и декодирование сообщения методом b1-R, b0-R
             (два младших бита красного канала).
"""

import os

try:
    from lab3 import ui
    from lab3.blue_decoder import decode_blue_channel
    from lab3.key_parser import save_keys
    from lab3.red_bits_codec import (
        capacity_in_chars,
        decode_message,
        encode_message,
        generate_key,
        load_image,
    )
except ImportError:
    import ui
    from blue_decoder import decode_blue_channel
    from key_parser import save_keys
    from red_bits_codec import (
        capacity_in_chars,
        decode_message,
        encode_message,
        generate_key,
        load_image,
    )

BASE_DIR = os.path.dirname(__file__)
DEFAULT_IMAGE_PATH = os.path.join(BASE_DIR, "data", "new14.png")
DEFAULT_KEYS_PATH = os.path.join(BASE_DIR, "data", "keys14.txt")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")


DEFAULT_MESSAGE = "Привет, меня зовут Полина Комиссарова, это тестовое сообщение."


def task_decode():
    """Задание 1.1: декодирование сообщения из синего канала."""
    print("\n--- Задание 1.1: декодирование сообщения ---")
    print(f"Изображение: {DEFAULT_IMAGE_PATH}")
    print(f"Файл ключа : {DEFAULT_KEYS_PATH}")

    try:
        message, coords = decode_blue_channel(
            DEFAULT_IMAGE_PATH, DEFAULT_KEYS_PATH
        )
    except Exception as error:
        print(f"Не удалось декодировать сообщение: {error}")
        return

    print(f"Использовано координат: {len(coords)}")
    print(f"Декодированное сообщение:\n{message}")


def print_encode_debug(debug_info):
    """Печатает отладочную информацию по первому символу сообщения."""
    print("\nОтладочная информация по первому символу сообщения:")
    print(f"  Символ            : {debug_info['char']!r}")
    print(f"  Биты байта символа: {debug_info['bits']}")
    print("  Исходные значения пикселей (R, G, B):")
    for pixel in debug_info["originals"]:
        print(f"    {pixel}")
    print("  Изменённые значения пикселей (R, G, B):")
    for pixel in debug_info["modified"]:
        print(f"    {pixel}")


def task_encode_decode():
    """Задание 1.2: кодирование и декодирование методом b1-R, b0-R."""
    print("\n--- Задание 1.2: кодирование методом b1-R, b0-R ---")

    try:
        image = load_image(DEFAULT_IMAGE_PATH)
    except Exception as error:
        print(f"Не удалось открыть изображение: {error}")
        return

    width, height = image.size
    max_chars = capacity_in_chars(width, height)
    print(f"Размер изображения: {width}x{height}")
    print(f"Максимум символов сообщения: {max_chars}")

    message = ui.ask_russian_message(DEFAULT_MESSAGE, max_chars)
    if message is None:
        print("Ввод прерван.")
        return

    try:
        coords = generate_key(width, height, len(message))
        encoded_image, debug_info = encode_message(image, message, coords)
    except Exception as error:
        print(f"Ошибка при кодировании: {error}")
        return

    print_encode_debug(debug_info)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    encoded_path = os.path.join(OUTPUT_DIR, "encoded_message.png")
    key_path = os.path.join(OUTPUT_DIR, "encoded_message_key.txt")

    try:
        encoded_image.save(encoded_path)
        save_keys(key_path, coords)
    except Exception as error:
        print(f"Не удалось сохранить результат: {error}")
        return

    print(f"\nЗакодированное изображение сохранено: {encoded_path}")
    print(f"Ключ (координаты пикселей) сохранён : {key_path}")

    decoded_back = decode_message(encoded_image, coords, len(message))
    print(f"\nПроверка декодированием обратно из изображения:")
    print(f"  Исходное сообщение    : {message}")
    print(f"  Декодированное обратно: {decoded_back}")
    print(
        "  Совпадает? "
        + ("Да" if decoded_back == message else "Нет (ошибка!)")
    )


def main():
    """Точка входа лабораторной работы №3."""
    print("=" * 60)
    print("Лабораторная №3. Стеганография. Вариант 14")
    print("=" * 60)

    while True:
        print("\nВыберите задание:")
        print("  1 - Декодировать сообщение из new14.png (синий канал)")
        print("  2 - Закодировать и декодировать своё сообщение (b1-R,b0-R)")
        print("  0 - Выход")

        try:
            choice = input("Ваш выбор: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if choice == "0":
            break
        elif choice == "1":
            task_decode()
        elif choice == "2":
            task_encode_decode()
        else:
            print("Нет такого пункта, выберите из списка.")

    print("Работа завершена.")


if __name__ == "__main__":
    main()
