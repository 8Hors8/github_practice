"""
    Модуль для обработки команд и сообщений Telegram-бота.
    Содержит классы и функции для взаимодействия с пользователями.
"""
import bot_msg, btn_text
from buttons import start_button


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
        def start_bot(message):
            self.handle_start(message)

        @self.bot.message_handler(commands=['help'])
        def help(message):
            self.handle_help(message)

        @self.bot.message_handler(func=lambda message: message.text == btn_text.BTN_STAR_GEME)
        def start_geme(message):
            self.handle_start_geme(message)

    def handle_start(self, message):
        """
            Обработка команды /start и отправляет приветственное сообщение.

            :param message : (telebot.types.Message) Сообщение от пользователя.
        """
        chat_id = message.chat.id
        self.bot.send_message(chat_id, bot_msg.MSG_START, reply_markup=start_button())

    def handle_help(self, message):
        """
           Обработка команды /help и отправляет сообщение с помощью.

           :param message : (telebot.types.Message) Сообщение от пользователя.
        """
        chat_id = message.chat.id
        self.bot.send_message(chat_id, bot_msg.MSG_HELP)

    def handle_start_geme(self, message):
        """
          Обработка кнопки BTN_STAR_GEME. Регистрирует пользователя
          в базе данных и отправляет приветственное сообщение.

          :param message : (telebot.types.Message) Сообщение от пользователя.
        """
        chat_id = message.chat.id
        self.bot.send_message(chat_id, 'Да начнется игра')
