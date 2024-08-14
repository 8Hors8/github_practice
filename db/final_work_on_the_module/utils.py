"""
    Этот модуль содержит утилиты для игрового процесса и взаимодействия с базой данных.
    Включает классы для управления игровым процессом и базой данных, а также функции
    для работы с пользователями и словами.
"""
import logging
from database import Database
from config import config_logging
from buttons import translation_buttons

logger = logging.getLogger('utils')
config_logging()


class GameUtils:
    """
          Класс с утилитами для игрового процесса.
    """

    def __init__(self, bot):
        self.bot = bot
        self.db = DatabaseUtils()

    def get_user_name(self, message):
        """
        Запрашивает имя пользователя и сохраняет его в базе данных.

        :param bot: Объект Telegram-бота для отправки сообщений.
        :param message: Сообщение от пользователя, содержащее его имя.
        """
        chat_id = message.chat.id
        self.bot.send_message(chat_id, 'Как я могу к вам обращаться?')
        self.bot.register_next_step_handler(message, self.save_user_name)

    def save_user_name(self, message):
        """
        Сохраняет имя пользователя и начинает игру.

        :param message: Сообщение от пользователя, содержащее его имя.
        """
        chat_id = message.chat.id
        print(message.from_user.id)
        user_name = message.text

        self.db.seve_user(user_name)

        self.bot.send_message(chat_id, f"Приятно познакомиться, {user_name}!\n Да начнется игра!!")
        self.start_game(message)

    def start_game(self, message):
        """
        Начинает игру, предлагая слово и варианты перевода.

        :param message: Объект Telegram-бота для отправки сообщений.
        """
        chat_id = message.chat.id
        word = "Мир"
        text_buttons = ["Tree", "Book", "vata"]
        correct_translation = "World"
        text_buttons.append(correct_translation)

        markup = translation_buttons(text_buttons)

        self.bot.send_message(chat_id, f"Как перевести слово '<b>{word}</b>'?",
                              reply_markup=markup, parse_mode="HTML")
        self.bot.register_next_step_handler_by_chat_id(chat_id, self.check_answer, correct_translation)

    def check_answer(self, message, correct_translation):
        """
        Проверяет правильность ответа пользователя.

        :param message: Сообщение от пользователя с его выбором.
        :param correct_translation: str Правильный перевод.
        """
        chat_id = message.chat.id
        user_answer = message.text

        if user_answer == correct_translation:
            self.bot.send_message(chat_id, "Превосходно! Вы справились! 🌟 +1 балл!")
            self.start_game(message)
        else:
            self.bot.send_message(chat_id, "Не совсем так. Но не отчаивайтесь! 💔 -3 балла!")
            self.start_game(message)


class DatabaseUtils(Database):
    def __init__(self):
        super().__init__()

    def add_tabl(self):
        """
           Создает необходимые таблицы в базе данных:
           - users: информация о пользователях.
           - word: информация о словах и их переводах.
           - users_word: связь пользователей и слов, а также количество показов каждого слова.
       """
        table_name_user = 'users'
        columns_user = [
            ('id', 'SERIAL PRIMARY KEY'),
            ('telegram_user_id', 'BIGINT NOT NULL UNIQUE'),
            ('name', 'VARCHAR(255)'),
            ('points', 'INTEGER DEFAULT 0')
        ]

        table_name_word = 'word'
        columns_word = [
            ('id', 'SERIAL PRIMARY KEY'),
            ('russian_words', 'VARCHAR(255)'),
            ('translation', 'VARCHAR(255)'),

        ]

        table_name_user_word = 'users_word'
        columns_user_word = [
            ('id', 'SERIAL PRIMARY KEY'),
            ('user_id', 'INTEGER REFERENCES users(id) ON DELETE CASCADE'),
            ('word_id', 'INTEGER REFERENCES word(id) ON DELETE CASCADE'),
            ('times_shown', 'INTEGER DEFAULT 0')
        ]

        self.create_table(table_name_user, columns_user)
        self.create_table(table_name_word, columns_word)
        self.create_table(table_name_user_word, columns_user_word)

    def seve_user(self, name):
        logger.info(f'Пользователь с именем {name} попал в базу')


if __name__ == '__main__':
    r = DatabaseUtils()
    r.add_tabl()
