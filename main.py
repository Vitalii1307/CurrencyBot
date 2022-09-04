import requests
import telebot
import random
from bs4 import BeautifulSoup as b

from telebot import types
URL_DOLLAR = 'https://kurs.com.ua/valyuta/usd'
URL_EURO = 'https://kurs.com.ua/valyuta/eur'
TOKEN = '5767694283:AAHhRMiq1nePLZe2wSERHaufYaiktmCzfR4'

bot = telebot.TeleBot(TOKEN)


def parser(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    prices_purches = soup.find_all('div', class_='course')[0]
    prices_sell = soup.find_all('div', class_='course')[1]
    priceForPurches = [c.text for c in prices_purches]
    priceForSell = [c.text for c in prices_sell]
    list = [priceForPurches[0], priceForSell[0]]
    return list

list_of_price_for_dollar = parser(URL_DOLLAR)
list_of_price_for_euro = parser(URL_EURO)
print(list_of_price_for_dollar)
print(list_of_price_for_euro)

@bot.message_handler(commands = ['start'])

def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('🎰Random number')
    item2 = types.KeyboardButton('📈Exchange rates')
    item3 = types.KeyboardButton('📒Info')

    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, 'Hello, {0.first_name}!'.format(message.from_user), reply_markup = markup)

@bot.message_handler(content_types = ['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == '🎰Random number':

            bot.send_message(message.chat.id, 'Your numbar: ' + str(random.randint(0, 1000)))

        elif message.text == '📈Exchange rates':

            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('Dollar, $')
            item2 = types.KeyboardButton('Euro, €')
            back = types.KeyboardButton('🔙Back')

            markup.add(item1, item2, back)
            bot.send_message(message.chat.id, '📈Exchange rates', reply_markup = markup)

        elif message.text == '🔙Back':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('🎰Random number')
            item2 = types.KeyboardButton('📈Exchange rates')
            item3 = types.KeyboardButton('📒Info')

            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id, '🔙Back, {0.first_name}!'.format(message.from_user), reply_markup = markup)

        elif message.text == 'Dollar, $':
            bot.send_message(message.chat.id, f'($): Buying/selling: {list_of_price_for_dollar[0]}' + '/' + f'{list_of_price_for_dollar[1]} (UAH)')

        elif message.text == 'Euro, €':
            bot.send_message(message.chat.id, f'(€): Buying/selling: {list_of_price_for_euro[0]}' + '/' + f'{list_of_price_for_euro[1]} (UAH)')





bot.polling(none_stop= True)