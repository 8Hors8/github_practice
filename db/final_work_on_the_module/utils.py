"""
    Этот модуль содержит утилиты для игрового процесса и взаимодействия с базой данных.
    Включает классы для управления игровым процессом и базой данных, а также функции
    для работы с пользователями и словами.
"""
import csv
import logging
import random

from database import Database
from config import config_logging
from buttons import translation_buttons

logger = logging.getLogger('utils')
config_logging()


class GameUtils:
    """
        Класс с утилитами для игрового процесса.

        Attributes:
            bot (telebot.TeleBot): Объект Telegram-бота для взаимодействия с Telegram API.
            db (DatabaseUtils): Объект для взаимодействия с базой данных.
    """

    def __init__(self, bot):
        self.bot = bot
        self.db = DatabaseUtils()

    def get_user_name(self, message):
        """
        Запрашивает имя пользователя и сохраняет его в базе данных.

        :param message: Сообщение от пользователя, содержащее его имя.
        """
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_info = self.db.search_user(user_id)
        if user_info is None:
            self.bot.send_message(chat_id, 'Как я могу к вам обращаться?')
            self.bot.register_next_step_handler(message, self.save_user_name)
        else:
            self.bot.send_message(chat_id, 'Игра продолжается!!')
            self.start_game(message)

    def save_user_name(self, message):
        """
        Сохраняет имя пользователя и начинает игру.

        :param message: Сообщение от пользователя, содержащее его имя.
        """
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_name = message.text

        self.db.save_user(user_name, user_id)

        self.bot.send_message(chat_id, f"Приятно познакомиться, {user_name}!\n Да начнется игра!!")
        self.start_game(message)

    def start_game(self, message):
        """
        Начинает игру, предлагая слово и варианты перевода.

        :param message: Объект Telegram-бота для отправки сообщений.
        """
        chat_id = message.chat.id
        word, correct_translation, text_buttons = self.word_generator(message)

        text_buttons.append(correct_translation)

        markup = translation_buttons(text_buttons)

        self.bot.send_message(chat_id, f"Как перевести слово '<b>{word}</b>'?",
                              reply_markup=markup, parse_mode="HTML")

        self.bot.register_next_step_handler_by_chat_id(chat_id, self.check_answer,
                                                       correct_translation)

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

    def word_generator(self, message):
        """
        Генерирует слова для перевода и соответствующие варианты перевода.

        Эта функция выбирает случайный источник слов (из CSV-файла или базы данных),
        а затем извлекает одно слово и его перевод. Также она генерирует список
        неправильных вариантов перевода для использования в качестве кнопок выбора.

        :param message: Объект сообщения от пользователя в Telegram, используемый
                        для получения ID пользователя.

        :return: Кортеж, содержащий выбранное слово, его правильный перевод и
                 список неправильных вариантов перевода.
        """
        id_user = message.from_user.id
        flag = random.randint(0, 1)
        if flag == 0:
            word_dicr = self.read_words_csv(id_user)

        else:
            word_dicr = self.read_words_bd(id_user)

        word = list(word_dicr.keys())[0]
        translation = word_dicr[word]
        text_buttons = list(word_dicr.values())[1:]
        return word, translation, text_buttons

    def read_words_csv(self, user_id: int, quantity: int = 4):
        """
            Читает указанное количество уникальных слов из CSV-файла,
            проверяет их на дубликаты в базе данных, сохраняет найденные слова вместе
            с их английскими переводами в словаре и удаляет выбранные слова из CSV-файла.

            :param user_id: ID пользователя в Telegram.
            :param quantity: Необязательный параметр, определяющий требуемое количество слов
                             для чтения (по умолчанию 4).

            :return words_dict: dict Словарь, содержащий русские слова в качестве ключей
                                и их английские переводы в качестве значений.
        """
        words_dict = {}
        try:
            with open('russian_english_words.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                words = list(reader)

            selected_words = random.sample(words[1:],
                                           len(words[1:]) if len(words[1:]) < quantity else quantity)

            for word_list in selected_words:
                check_word_bd = self.db.search_word(word_list[0])
                if check_word_bd is None:
                    self.db.save_word(word_list[0], word_list[1])

                words_dict[word_list[0]] = word_list[1]

            if len(words_dict) < quantity:
                result = self.db.get_random_words_for_user(user_id, quantity - len(words_dict))
                words_dict.update(result)

            remaining_words = [word for word in words if word not in selected_words]
            with open('russian_english_words.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                for word in remaining_words:
                    writer.writerow(word)

            return words_dict

        except Exception as e:
            logger.error(f'ошибка {e}')
            words_dict.update(self.read_words_bd(user_id))
            return words_dict

    def read_words_bd(self, user_id):
        """
        Запрашивает слова с переводом из базы данных.

        Эта функция запрашивает слова, которые пользователь еще не видел 4 раза,
        из базы данных. Если найденных слов меньше необходимого количества,
        оставшиеся слова выбираются из CSV-файла.

        :param user_id: ID пользователя в Telegram.

        :return: dict Словарь, содержащий русские слова в качестве ключей и их
                 английские переводы в качестве значений.
        """
        rusult = self.db.get_random_words_for_user(user_id)

        if len(rusult) < 4:
            csv_word = self.read_words_csv(user_id, 4 - len(rusult))
            rusult.update(csv_word)
        return rusult


class DatabaseUtils(Database):
    """
       Класс для управления базой данных, наследующий методы и свойства из класса Database.
    """

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

    def save_user(self, name, tg_user_id):
        """
        Сохраняет информацию о пользователе в базе данных.

        Функция сохраняет имя пользователя и его уникальный идентификатор в Телеграме
        в таблицу `users` базы данных.

        :param name: str Имя пользователя, указанное в Телеграме.
        :param tg_user_id: int Идентификатор пользователя в Телеграме.
        """
        table_name = 'users'
        data = {
            'telegram_user_id': tg_user_id,
            'name': name
        }
        self.insert_data(table_name=table_name, data=data)

    def search_user(self, tg_user_id):
        """
        Ищет информацию о пользователе в базе данных по его Telegram ID.

        Функция выполняет запрос в таблицу `users`, чтобы найти пользователя по его
        идентификатору в Телеграме. Если пользователь найден, возвращает словарь с
        информацией о пользователе (ID, имя, очки). В противном случае возвращает `None`.

        :param tg_user_id: int Идентификатор пользователя в Телеграме.

        :return: dict Словарь с информацией о пользователе (ID, имя, очки) или `None`,
                      если пользователь не найден.
        """
        table_name = 'users'
        columns = 'id,name,points'
        values = (tg_user_id,)
        condition = 'telegram_user_id = %s'
        result = self.select_data(table_name=table_name, columns=columns,
                                  values=values, condition=condition)
        if result:
            user_info = {
                'id': result[0][0],
                'name': result[0][1],
                'points': result[0][2]
            }
        else:
            user_info = None
        return user_info

    def search_word(self, word):
        """
        Ищет слово в базе данных.

        Функция выполняет запрос в таблицу `word`, чтобы найти слово по его русскому написанию.
        Если слово найдено, возвращает его ID. В противном случае возвращает `None`.

        :param word: str Слово на русском языке, которое нужно найти.

        :return: int Идентификатор слова в базе данных или `None`, если слово не найдено.
        """
        table_name = 'word'
        condition = 'russian_words = %s'

        result = self.select_data(table_name, 'id',
                                  condition=condition, values=(word,))
        if result:
            answer = result[0][0]
        else:
            answer = None
        return answer

    def save_word(self, word, translation):
        """
        Сохраняет слово и его перевод в базе данных.

        Функция сохраняет русское слово и его английский перевод в таблицу `word` базы данных.

        :param word: str Слово на русском языке.
        :param translation: str Перевод слова на английский язык.
        """
        data = {
            'russian_words': word,
            'translation': translation
        }
        table_name = 'word'
        self.insert_data(table_name, data)

    def get_random_words_for_user(self, user_id: int, quantity: int = 4):
        """
            Извлекает случайные слова для указанного пользователя, которые были показаны менее
            4 раз, и возвращает их в виде словаря.

            Функция выбирает слова, которые еще не были показаны пользователю 4 и более раз,
            и ограничивает выбор указанным количеством (по умолчанию 4).
            Результаты выбираются случайным образом и возвращаются в виде словаря,
            где ключами являются слова на русском языке, а значениями их переводы на английский.

            :param user_id: int Идентификатор пользователя в базе данных.
            :param quantity: int Количество случайных слов для выбора (по умолчанию 4).

            :return: dict Словарь с выбранными словами, где ключами являются русские слова,
                   а значениями их переводы на английский.
        """

        words_dict = {}
        table_name = 'word w'
        columns = 'w.russian_words, w.translation'
        condition = f"""
            w.id NOT IN (
                SELECT uw.word_id
                FROM users_word uw
                WHERE uw.user_id = {user_id}
                GROUP BY uw.word_id
                HAVING SUM(uw.times_shown) >= 4
            )
            ORDER BY RANDOM()
            LIMIT {quantity};        
        """

        result_bd_word = self.select_data(table_name=table_name,
                                          columns=columns,
                                          condition=condition
                                          )
        for words in result_bd_word:
            words_dict[words[0]] = words[1]

        return words_dict


if __name__ == '__main__':
    pass
