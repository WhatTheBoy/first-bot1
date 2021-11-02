import requests
import json
import time
import config
import schedule
import math
from tkinter import *
import pywhatkit as kit
from threading import *

from telebot import *





bot = telebot.Telebot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    buttonA = types.KeyboardButton('A')
    buttonB = types.KeyboardButton('B')
    buttonC = types.KeyboardButton('C')

    markup.row(buttonA, buttonB)
    markup.row(buttonC)

    bot.send_message(message.chat.id, 'It works!', reply_markup=markup)

def answer_user_bot(data):
    data = {
        'chat_id': config.MY_ID,
        'text': data
    }
    url = config.URL.format(
        token=config.TOKEN,
        method=config.SEND_METH
    )
    response = requests.post(url, data=data)
    print(response)

def parse_weather_data(data):
    for elem in data['weather']:
        weather_state = elem['main']
    temp = round(data['main']['temp'] - 273.15 ,2)
    city = data['name']
    msg = f'The weather in {city}: Temp is {temp}, State is {weather_state}'
    return msg

def get_weather(location):
    url = config.WEATHER_URL.format(city=location,
                                    token=config.WEATHER_TOKEN)
    response = requests.get(url)
    if response.status_code != 200:
        return 'city not found'
    data = json.loads(response.content)
    return parse_weather_data(data)


def get_message(data):
    return data['message']['text']

def save_update_id(update):
    with open(config.UPDATE_ID_FILE_PATH, 'w') as file:
        file.write(str(update['update_id']))
    return True

def main():
    while True:
        schedule.run_pending()
        time.sleep(1)
        url = config.URL.format(token=config.TOKEN, method=config.UPDATE_METH)
        content = requests.get(url).text

        data = json.loads(content)
        result = data['result'][::-1]
        needed_part = None

        for elem in result:
            if elem['message']['chat']['id'] == config.MY_ID:
                needed_part = elem
                break

        if config.UPDATE_ID != needed_part['update_id']:
            message = get_message(needed_part)
            msg = get_weather(message)
            answer_user_bot(msg)
            save_update_id(needed_part)
        time.sleep(1)




city_name = 'Kyiv,Ukraine'
api_key = '6542053fff462483a3cf670e21f195dc'


def helper(api_key, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response2 = requests.get(url).json()
    temperature = round(response2['main']['temp']- 273.15, 2)
    feels_like = round(response2['main']['feels_like']-273.15,2)
    humidity = response2['main']['humidity']
    print('Сейчас температура:',temperature )
    schedule.every(10).seconds.do(helper, api_key, city_name)


t2 = Thread(target=helper, args=(api_key, city_name))
t2.start()
t2.join()
t2.deamon = True

t1 = Thread(target=main)
t1.start()
t1.join()
t1.deamon = True


bot.polling()