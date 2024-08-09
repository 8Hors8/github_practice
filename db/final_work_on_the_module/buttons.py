"""
    Модуль для создания различных кнопок для Telegram-бота.
    Содержит функции для генерации кнопок с помощью классов клавиатур.
"""

from keyboard import ReplyKeyboard, InlineKeyboard
from telebot import types


def test_button():
    """
        Функция для создания тестовой клавиатуры с кнопками.

        :return:
            ReplyKeyboard: Объект клавиатуры с тестовыми кнопками.
    """
    reply_keyboard = ReplyKeyboard(resize_keyboard=True, row_width=2)
    reply_keyboard.add_button(types.KeyboardButton('Кнопка 1'), types.KeyboardButton('Кнопка 2'))
    reply_keyboard.add_row(types.KeyboardButton('Кнопка 3'), types.KeyboardButton('Кнопка 4'))

    return reply_keyboard.get_markup()



