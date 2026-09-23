"""Получение текущего часа (по времени Нижнего Новгорода = МСК).

Задание требует, чтобы нужная информация парсилась с подходящего
веб-сайта. Час извлекается регулярным выражением из ответа сервиса
точного времени. Если сайт недоступен (нет сети, сайт лёг и т.п.),
используется резервный вариант - локальное время по часовому поясу
Europe/Moscow, чтобы бот не падал и не переставал отвечать.
"""

import re
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

# WorldTimeAPI отдаёт JSON с полем "datetime": "2026-09-23T10:15:00+03:00"
TIME_API_URL = "https://worldtimeapi.org/api/timezone/Europe/Moscow"
REQUEST_TIMEOUT = 5  # секунд

# Ищем час сразу после даты и буквы T в строке datetime.
HOUR_PATTERN = re.compile(r'"datetime":\s*"\d{4}-\d{2}-\d{2}T(\d{2}):')

FALLBACK_TIMEZONE = ZoneInfo("Europe/Moscow")


def fetch_hour_from_web(url=TIME_API_URL, timeout=REQUEST_TIMEOUT):
    """Запрашивает текущее время с сайта и извлекает час регулярным
    выражением. При любой проблеме бросает исключение - обработка
    (резервный вариант) выполняется в get_current_hour().
    """
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()

    match = HOUR_PATTERN.search(response.text)
    if not match:
        raise ValueError("Не удалось найти время в ответе сервера")

    return int(match.group(1))


def get_current_hour():
    """Возвращает текущий час (0-23) в Нижнем Новгороде.

    Сначала пробует получить время с веб-сайта, при любой ошибке
    (нет сети, сайт недоступен, неожиданный ответ) использует
    локальное время по часовому поясу Europe/Moscow.
    """
    try:
        return fetch_hour_from_web()
    except Exception:
        return datetime.now(FALLBACK_TIMEZONE).hour
