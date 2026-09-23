"""Лабораторная работа №1. Вариант 14.

Задание: извлечение чисел из строки, содержащей числа и буквы.

Ограничения лабораторной: модули НЕ импортируются (поэтому без re),
обязательно используется lambda-функция, ввод с клавиатуры.
"""

DIGITS = "0123456789"
YES_ANSWERS = ("да", "д", "yes", "y")
NO_ANSWERS = ("нет", "н", "no", "n")


def to_number(chunk):
    """Преобразует строку из цифр в целое число.

    Если число настолько длинное, что Python отказывается его
    преобразовывать, оставляет его строкой, чтобы программа не упала.
    """
    try:
        return int(chunk)
    except ValueError:
        return chunk


def extract_numbers(text):
    """Возвращает список чисел, найденных в строке.

    Пример: "abc12de345" -> [12, 345]
    """
    # lambda: цифру оставляем, любой другой символ заменяем пробелом
    cleaned = "".join(map(lambda ch: ch if ch in DIGITS else " ", text))
    # split() без аргументов склеивает подряд идущие пробелы,
    # остаются только группы цифр
    return list(map(to_number, cleaned.split()))


def read_line(prompt):
    """Безопасный ввод строки. Возвращает None при Ctrl+C / Ctrl+D."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def ask_text():
    """Запрашивает непустую строку, пока пользователь не введёт её."""
    while True:
        text = read_line("Введите строку с числами и буквами: ")
        if text is None:
            return None
        if text.strip() == "":
            print("Вы ничего не ввели. Попробуйте ещё раз.\n")
            continue
        return text


def ask_repeat():
    """Спрашивает, повторить ли работу. True - повторить."""
    while True:
        answer = read_line("Хотите ввести другую строку? (да/нет): ")
        if answer is None:
            return False
        answer = answer.strip().lower()
        if answer in YES_ANSWERS:
            print()
            return True
        if answer in NO_ANSWERS:
            return False
        print("Пожалуйста, ответьте «да» или «нет».")


def main():
    """Точка входа лабораторной работы №1."""
    print("=" * 50)
    print("Лабораторная №1. Извлечение чисел из строки")
    print("Пример ввода: abc12de345  ->  результат: [12, 345]")
    print("=" * 50)

    while True:
        text = ask_text()
        if text is None:
            break

        numbers = extract_numbers(text)
        if not numbers:
            print("В строке нет ни одной цифры. Попробуйте ещё раз.\n")
            continue

        print(f"Исходная строка : {text}")
        print(f"Найдено чисел   : {len(numbers)}")
        print(f"Числа           : {numbers}")
        print(f"Через пробел    : {' '.join(map(str, numbers))}")
        print()

        if not ask_repeat():
            break

    print("Работа завершена.")


if __name__ == "__main__":
    main()
