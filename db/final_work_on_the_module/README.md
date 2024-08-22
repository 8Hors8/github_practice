# Bot Guessing Game

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-310/)

Bot Guessing Game - это Telegram-бот, который помогает пользователям учить английские слова, предлагая им угадывать переводы слов. 
Проект поддерживает систему начисления очков, ведет учет рейтинга пользователей, и предоставляет возможность использовать слова из базы данных или CSV-файла.

## Оглавление
- [Функциональность](#функциональность)
- [Установка](#установка)
- [Настройка](#настройка)
- [Запуск](#запуск)
- [Примеры использования](#примеры-использования)
- [Структура проекта](#структура-проекта)
- [Контакты](#контакты)

## Функциональность

- Поддержка многоразового использования слов (до 4 раз)
- Автоматическое начисление и вычитание очков за правильные и неправильные ответы
- Хранение данных о пользователях и словах в базе данных PostgreSQL
- Импорт слов из CSV-файла
- Отображение рейтинга пользователей

## Установка

1. Клонируйте репозиторий на ваше устройство:
    ```bash
    git clone https://github.com/8Hors8/bot_guessing-game.git
    ```
2. Перейдите в папку проекта:
    ```bash
    cd bot_guessing-game
    ```
3. Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`
    ```
4. Установите необходимые зависимости:
    ```bash
    pip install -r requirements.txt
    ```

## Настройка

1. Создайте файл `token.env` в корне проекта, где будут храниться ваши конфиденциальные данные:
    ```ini
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    dbname = Название базы данных
    dbuser = Имя пользователя
    password = Пароль
    ```
    - `TELEGRAM_BOT_TOKEN`: Токен вашего Telegram-бота, который можно получить через BotFather.    

2. Бот автоматически создат нужные талицы в базе данных.

3. Для добавление слов можно создать CSV файл в корнейвой папке названием russian_english_words.csv в котором должны содержать
   слова в формате "russian_word,english_word"

## Запуск

1. Запустите бота:
    ```bash
    python main.py
    ```

2. Бот будет ждать сообщений в Telegram и реагировать на команды.

## Примеры использования

1. Запустите бота в Telegram, отправив `/start`.
2. Следуйте инструкциям бота: он спросит ваше имя и начнет игру.
3. Выберите правильный перевод слова из предложенных вариантов.
4. Просматривайте свой рейтинг, используя команду `/rating`.

## Структура проекта

- `main.py`: Основной файл для запуска бота.
- `handlers.py`: Обработка команд и сообщений от пользователей.
- `keyboard.py`: Создание и настройка кнопок для интерфейса бота.
- `config.py`: Настройка конфигурации проекта, включая логирование и загрузку переменных окружения.
- `utils.py`: Вспомогательные утилиты, включая функции для обработки слов и работы с базой данных.
- `init.sql`: SQL-скрипт для инициализации базы данных.
- `requirements.txt`: Список зависимостей проекта.
- `README.md`: Описание проекта.

## Контакты

Если у вас есть вопросы или предложения, вы можете связаться со мной через Telegram: [@8Hors8](https://t.me/8Hors8).