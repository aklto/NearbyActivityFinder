import telebot
import redis

# import mysql
from telebot import types
from API_Token.API_Token import *
from TripadvisorAPI.TripadvisorAPI import *
from googletrans import Translator

translator = Translator()

text = "Привет, мир!"
translated = translator.translate(text, dest='ru')

print(translated.text)



r = redis.StrictRedis(host='localhost', port=6379, db=1)
r.set("coefficient", 0)

class What_Your_Location:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.add_handlers()

    def start(self, message):
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
        keyboard.add(button_geo)

        self.bot.send_message(message.chat.id, "Добрый день, я бот который ищет активности вокруг вас, воспользуйтесь меню для начала работы")
        self.bot.send_message(message.chat.id, "Поделись местоположением для моей работы", reply_markup=keyboard)

    def location(self, message):
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        Button_menu = types.KeyboardButton('меню🏠')
        Button_next = types.KeyboardButton('👎')
        Button_like = types.KeyboardButton('👍')
        keyboard.add(Button_menu, Button_next, Button_like)

        r.set(str(message.chat.id)+"latitude", message.location.latitude)
        r.set(str(message.chat.id) + "longitude", message.location.longitude)

        self.bot.send_message(message.chat.id, "выберите", reply_markup=keyboard)

    def user_text(self, message):
        if message.text == '👍':
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            Button_menu = types.KeyboardButton('меню🏠')
            keyboard.add(Button_menu)

            self.bot.send_message(message.chat.id, 'Отличный выбор, хорошего вечера', reply_markup=keyboard)

        elif message.text == '👎':
            nearby_restaurants_id = Excerpt_From_Dictionary_Nearby(float(r.get(str(message.chat.id) + "latitude")),
                                                                   float(r.get(str(message.chat.id) + "longitude")),
                                                                   TRIPADVISOR_KEY, "restaurants", "location_id",
                                                                   int(r.get("coefficient")))

            id_restaurants_to_detalis = Excerpt_From_Dictionary_details(str(nearby_restaurants_id.response_nearby()),
                                                                      TRIPADVISOR_KEY, "restaurants", "location_id")

            original_photos = [item['images']['original']['url'] for item in id_restaurants_to_detalis.response_photo()]

            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            Button_menu = types.KeyboardButton('меню🏠')
            Button_next = types.KeyboardButton('👎')
            Button_like = types.KeyboardButton('👍')
            keyboard.add(Button_menu, Button_next, Button_like)

            media = [types.InputMediaPhoto(url) for url in original_photos]

            self.bot.send_media_group(message.chat.id, media)
            print(id_restaurants_to_detalis.response_details())

            details = id_restaurants_to_detalis.response_details()

            name = details['name'] if 'name' in details else "-"
            description = details['description'] if 'description' in details else "-"
            rating = details['rating'] if 'rating' in details else "-"


            translated_description = translator.translate(description, dest='ru')

            result = (f"Название: {name}\n"
                      f"\nОписание: {translated_description.text}\n"
                      f"\nРэйтинг: {rating}")

            self.bot.send_message(message.chat.id,result)

            r.incr("coefficient", 1)

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
