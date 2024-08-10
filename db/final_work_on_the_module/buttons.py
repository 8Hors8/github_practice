"""
    Модуль для создания различных кнопок для Telegram-бота.
    Содержит функции для генерации кнопок с помощью классов клавиатур.
"""
import btn_text
from keyboard import ReplyKeyboard, InlineKeyboard
from telebot import types


def start_button():
    """
        Функция для создания стартовой клавиатуры с кнопками.

        :return:
            ReplyKeyboard: Объект клавиатуры .
    """
    reply_keyboard = ReplyKeyboard(resize_keyboard=True, row_width=1)
    reply_keyboard.add_button(types.KeyboardButton(btn_text.BTN_STAR_GEME))

    return reply_keyboard.get_markup()
