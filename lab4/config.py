"""Загрузка конфигурации бота (токен) из файла .env.

Токен не хранится в коде - это небезопасно, особенно если код
выкладывается на GitHub. Вместо этого он читается из файла .env,
который НЕ должен попадать в git (см. .gitignore в корне проекта).
"""

import os

from dotenv import load_dotenv

load_dotenv()

TOKEN_ENV_VAR = "TELEGRAM_BOT_TOKEN"


def get_bot_token():
    """Возвращает токен бота из .env или None, если он не задан."""
    token = os.getenv(TOKEN_ENV_VAR)
    if token:
        token = token.strip()
    return token or None
