"""Лабораторная работа №4. Вариант 14.

Telegram-бот, который здоровается в зависимости от времени суток.
Username бота: ist_24_2_var14_bot

Запуск: python lab4/main.py (или пункт меню в корневом main.py).
Требуется файл .env с переменной TELEGRAM_BOT_TOKEN (см. .env.example).
"""

try:
    from lab4 import config, handlers
except ImportError:
    import config
    import handlers

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
)


def build_application(token):
    """Собирает приложение бота: регистрирует все обработчики."""
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(CommandHandler("help", handlers.help_command))
    application.add_handler(
        CallbackQueryHandler(
            handlers.greet_callback,
            pattern=f"^{handlers.GREET_CALLBACK_DATA}$",
        )
    )
    application.add_error_handler(handlers.error_handler)

    return application


def main():
    """Точка входа лабораторной работы №4."""
    token = config.get_bot_token()
    if token is None:
        print(
            "Не найден токен бота. Создайте файл .env в корне проекта "
            "со строкой:\n"
            "TELEGRAM_BOT_TOKEN=ваш_токен_от_BotFather\n"
            "(пример - в файле .env.example)"
        )
        return

    print("Бот запускается... Username: ist_24_2_var14_bot")
    print("Для остановки нажмите Ctrl+C")

    application = build_application(token)
    try:
        application.run_polling()
    except Exception as error:
        print(f"Бот остановлен из-за ошибки: {error}")


if __name__ == "__main__":
    main()
