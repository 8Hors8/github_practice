"""
    Модуль для обработки команд и сообщений Telegram-бота.
    Содержит классы и функции для взаимодействия с пользователями.
"""

from buttons import test_button

class Handlers:
    """
        Класс для настройки и обработки команд Telegram-бота.

        Attributes:
            bot (telebot.TeleBot): Объект бота для взаимодействия с Telegram API.
            db (Database): Объект для взаимодействия с базой данных.
            user_model (User): Модель для работы с пользователями.
            lesson_model (Lesson): Модель для работы с уроками.
    """

    def __init__(self, bot):
        """
            Инициализация обработчика команд и баз данных.

            :param bot (telebot.TeleBot): Объект бота для взаимодействия с Telegram API.
        """
        self.bot = bot
        self.setup_handlers()

    def setup_handlers(self):
        """
            Настройка обработчиков команд.
        """
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.handle_start(message)

    def handle_start(self, message):
        """
            Обработка команды /start. Регистрирует пользователя
            в базе данных и отправляет приветственное сообщение.

            :param message (telebot.types.Message): Сообщение от пользователя.
        """
        chat_id = message.chat.id
        self.bot.send_message(chat_id, 'Привет выбери кнопку',reply_markup=test_button())