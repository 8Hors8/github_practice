"""
    Модуль для настройки конфигурации проекта.
    Содержит функции для загрузки токенов и настройки логирования.
"""
import logging
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='./token.env')

TELEBOT_TOKEN = os.getenv('BOT_API_TOKEN')


# YANDEX_API_KEY = os.getenv('YANDEX_API_KEY')
# DB_PATH = os.getenv('DB_PATH', 'database.db')


def config_logging(level=logging.INFO):
    """
        Настройка логирования для приложения.
        :param level (int): Уровень логирования. По умолчанию - INFO.
    """
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)s:%(lineno)d %(levelname)7s - %(message)s"

    )
