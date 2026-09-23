"""Общее меню запуска лабораторных работ (вариант 14)."""

import importlib

# Номер лабы -> (название, модуль). Новые лабы добавляются сюда.
LABS = {
    "1": ("Лаб 1. Извлечение чисел из строки", "lab1.main"),
    "2": ("Лаб 2. Спектральный анализ речевого сигнала", "lab2.main"),
    "3": ("Лаб 3. Стеганография", "lab3.main"),
    "4": ("Лаб 4. Telegram-бот", "lab4.main"),
}


def run_lab(module_name):
    """Импортирует модуль лабы и запускает его main()."""
    try:
        module = importlib.import_module(module_name)
        module.main()
    except ImportError as error:
        print(f"Не удалось загрузить лабу: {error}")
    except Exception as error:  # меню не должно падать из-за лабы
        print(f"Ошибка во время работы лабы: {error}")


def main():
    """Главное меню."""
    while True:
        print("\n===== Лабораторные работы, вариант 14 =====")
        for number, (title, _) in LABS.items():
            print(f"  {number} - {title}")
        print("  0 - Выход")

        try:
            choice = input("Ваш выбор: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if choice == "0":
            break
        if choice in LABS:
            run_lab(LABS[choice][1])
        else:
            print("Нет такого пункта, выберите из списка.")

    print("До свидания!")


if __name__ == "__main__":
    main()
