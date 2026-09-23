"""Консольный ввод данных для лабы 3 с проверкой регулярными выражениями."""

import re

# Только русский текст: буквы, цифры, пробелы и базовая пунктуация.
# Латинские буквы намеренно запрещены - кодирование ведём на русском.
RUSSIAN_MESSAGE_PATTERN = re.compile(
    r"^[А-Яа-яЁё0-9\s.,!?;:()\-]+$"
)

YES_ANSWERS = ("да", "д", "yes", "y")
NO_ANSWERS = ("нет", "н", "no", "n")


def read_line(prompt):
    """Безопасный ввод строки. Возвращает None при Ctrl+C / Ctrl+D."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def ask_yes_no(prompt):
    """Запрашивает ответ да/нет. Возвращает True/False/None (при обрыве)."""
    while True:
        answer = read_line(prompt)
        if answer is None:
            return None
        answer = answer.strip().lower()
        if answer in YES_ANSWERS:
            return True
        if answer in NO_ANSWERS:
            return False
        print("Пожалуйста, ответьте «да» или «нет».")


def ask_russian_message(default_message, max_length):
    """Запрашивает у пользователя текст на русском языке.

    Пустой ввод (просто Enter) принимает сообщение по умолчанию.
    Сообщение проверяется регулярным выражением: только русские
    буквы, цифры, пробелы и базовая пунктуация.
    """
    while True:
        raw = read_line(
            "Введите сообщение на русском языке для кодирования "
            f"(Enter - использовать пример: «{default_message}»): "
        )
        if raw is None:
            return None

        text = raw.strip()
        if text == "":
            text = default_message

        if not RUSSIAN_MESSAGE_PATTERN.match(text):
            print(
                "Сообщение должно содержать только русские буквы, "
                "цифры, пробелы и знаки препинания (. , ! ? ; : ( ) -). "
                "Латинские буквы и другие символы не поддерживаются.\n"
            )
            continue

        if len(text) > max_length:
            print(
                f"Сообщение слишком длинное: {len(text)} символов, "
                f"а изображение вмещает не более {max_length}. "
                f"Введите текст покороче.\n"
            )
            continue

        return text
