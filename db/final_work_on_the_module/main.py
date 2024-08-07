import telebot
import os
from dotenv import load_dotenv


# load_dotenv(dotenv_path='./token.env')
#
# api_token = os.getenv('BOT_API_TOKEN')

class Bot_star:
    def __init__(self, path):
        load_dotenv(dotenv_path=path)

        api_token = os.getenv('BOT_API_TOKEN')

        self.bot = telebot.TeleBot(api_token)

    def bot_polling(self):
        self.bot.polling()


if __name__ == '__main__':
    print('Bot star')
    bot = Bot_star('./token.env')
    bot.bot_polling()
