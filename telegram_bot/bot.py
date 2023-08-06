import telebot
import redis
import mysql
from telebot import types
from API_Token.API_Token import *
from TripadvisorAPI.TripadvisorAPI import *
class What_Your_Location:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.add_handlers()

    def start(self, message):
        chat_id = message.chat.id

        # Создание клавиатуры
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
        keyboard.add(button_geo)

        self.bot.send_message(message.chat.id, "Добрый день, я бот который ищет активности вокруг вас, воспользуйтесь меню для начала работы")
        self.bot.send_message(chat_id, "Поделись местоположением для моей работы", reply_markup=keyboard)

    def location(self, message):
        index_of_place = 0
        lat = message.location.latitude
        lon = message.location.longitude
        element1 = Excerpt_From_Dictionary_Nearby(lat, lon, TRIPADVISOR_KEY, "restaurants", "location_id", index_of_place)
        self.bot.send_message(message.chat.id, element1.response_nearby())

    def user_text(self, message):
        if message.text == '👍':
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            Button_menu = types.KeyboardButton('меню🏠')
            keyboard.add(Button_menu)
            self.bot.send_message(message.chat.id, 'Отличный выбор, хорошего вечера', reply_markup=keyboard)

        elif message.text == '':
            element1 = Excerpt_From_Dictionary_Nearby(lat, lon, TRIPADVISOR_KEY, "restaurants", "location_id",index_of_place)
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            Button_menu = types.KeyboardButton('меню🏠')
            Button_next = types.KeyboardButton('')
            Button_like = types.KeyboardButton('')
            keyboard.add(Button_menu, Button_next, Button_like)
            self.bot.send_message(message.chat.id, )

    def add_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            self.start(message)

        @self.bot.message_handler(content_types=['location'])
        def handle_location(message):
            self.location(message)

        @self.bot.message_handler(content_types=['text'])
        def button(message):
            self.user_text(message)

    def run(self):
        self.bot.polling()

if __name__ == "__main__":
    bot = What_Your_Location(BOT_TOKEN)
    bot.run()
