"""Обработчики команд /start, /help и кнопки приветствия."""

import re

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes

try:
    from lab4.greeting import greeting_for_hour
    from lab4.time_service import get_current_hour
except ImportError:
    from greeting import greeting_for_hour
    from time_service import get_current_hour

GREET_CALLBACK_DATA = "greet_me"

# Оставляем в имени только буквы, цифры, пробел и дефис - на случай,
# если у пользователя в Telegram стоит имя с эмодзи или спецсимволами,
# чтобы не отправлять их бездумно обратно в сообщении.
SAFE_NAME_PATTERN = re.compile(r"[^\w\s\-]", re.UNICODE)


def clean_name(raw_name):
    """Убирает из имени пользователя небезопасные символы (эмодзи и т.п.).

    Если после очистки имя пустое, возвращает нейтральное обращение.
    """
    if not raw_name:
        return "друг"
    cleaned = SAFE_NAME_PATTERN.sub("", raw_name).strip()
    return cleaned if cleaned else "друг"


def greet_keyboard():
    """Инлайн-клавиатура с единственной кнопкой приветствия."""
    button = InlineKeyboardButton(
        "Поприветствуй меня", callback_data=GREET_CALLBACK_DATA
    )
    return InlineKeyboardMarkup([[button]])


def build_greeting_text(raw_name):
    """Собирает текст приветствия для пользователя по текущему часу."""
    hour = get_current_hour()
    greeting = greeting_for_hour(hour)
    name = clean_name(raw_name)
    return f"{greeting}, {name}! Сейчас {hour} час(ов) по Нижнему Новгороду."


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start - приветствие пользователя по имени и времени суток."""
    user = update.effective_user
    text = build_greeting_text(user.first_name if user else None)
    await update.message.reply_text(text, reply_markup=greet_keyboard())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/help - справка по боту (с грустным смайликом, как требуется)."""
    text = (
        "Я бот, который здоровается в зависимости от времени суток. 😢\n\n"
        "Доступные команды:\n"
        "/start - поздороваться со мной\n"
        "/help - показать эту справку\n\n"
        "Также можно просто нажать кнопку «Поприветствуй меня»."
    )
    await update.message.reply_text(text, reply_markup=greet_keyboard())


async def greet_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатия кнопки «Поприветствуй меня».

    Если час с прошлого раза не изменился, новый текст будет точь-в-точь
    совпадать со старым, а Telegram запрещает редактировать сообщение
    "в то же самое" содержимое (ошибка "Message is not modified").
    Это не баг, а особенность API, поэтому такой случай отдельно
    отлавливается и превращается в дружелюбное всплывающее уведомление
    вместо падения в лог ошибок.
    """
    query = update.callback_query
    user = query.from_user
    text = build_greeting_text(user.first_name if user else None)

    if query.message is not None and query.message.text == text:
        await query.answer("Час не изменился - приветствие то же самое.")
        return

    try:
        await query.edit_message_text(text, reply_markup=greet_keyboard())
    except BadRequest as error:
        if "Message is not modified" not in str(error):
            raise

    await query.answer()


async def error_handler(update, context):
    """Общий обработчик ошибок - бот не должен падать ни при каких
    обстоятельствах, поэтому любая ошибка просто логируется.
    """
    print(f"Ошибка при обработке обновления: {context.error}")
