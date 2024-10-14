import requests
import telebot
import json
import re
from decouple import config

BOT_TOKEN = config('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

API_KEY = config('API_KEY')


def get_city_cords(city):
    """
        Retrieves the coordinates (latitude and longitude) of a given city from the OpenWeatherMap API.

        Args:
            city (str): The name of the city to retrieve coordinates for.

        Returns:
            dict or list or bool:
                - dict: Weather data for the city if found.
                - list: A list of possible matching cities if the exact city is not found.
                - bool: False if no matching cities are found.
    """
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=100&appid={API_KEY}'
    response = requests.get(url)
    if response.json() == []:
        return False
    result_city = response.json()[0]['name']
    if result_city.lower() == city.lower():
        lat = response.json()[0]['lat']
        lon = response.json()[0]['lon']
        return get_city_weather(lat, lon)
    else:
        result = []
        for count, i in enumerate(response.json(), start=1):
            city_info = {'name': i['name'], 'lat': i['lat'], 'lon': i['lon'], 'country': i['country']}
            result.append(f"{count}. {json.dumps(city_info)}")
        return result if result else False


def get_city_weather(lat, lon):
    """
        Retrieves the current weather data for a given location from the OpenWeatherMap API.

        Args:
            lat (float): The latitude of the location.
            lon (float): The longitude of the location.

        Returns:
            dict or bool:
                - dict: The current weather data for the location if the request is successful.
                - bool: False if the request fails (non-200 status code).
    """
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code != 200:
        return False
    data = response.json()
    return data


def select_town(message, data):
    """
    Handles the user's selection of a town from a list of options.

    Args:
        message (object): The user's message object.
        data (list): The list of town options.

    Returns:
        None
    """
    try:
        selected_town = int(message.text)
        if 1 <= selected_town <= len(data):
            city_info = json.loads(data[selected_town - 1].split('. ', 1)[1])
            city_weather = get_city_weather(city_info['lat'], city_info['lon'])
            if city_weather == False:
                bot.send_message(message.chat.id, 'Произошла ошибка, попробуйте ещё раз')
            get_weather_report(message, city_weather)
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, выберите корректный номер города.')
            bot.register_next_step_handler(message, select_town, data)
    except:
        bot.send_message(message.chat.id, 'Пожалуйста, введите число.')
        bot.register_next_step_handler(message, select_town, data)


def get_weather_report(message, data):
    """
    Sends a weather report message to the user.

    Args:
        message (object): The user's message object.
        data (dict): The weather data for the location.

    Returns:
        None
    """
    bot.send_message(message.chat.id,
                     f'В городе {data["name"]} сейчас {data["weather"][0]["description"]}, '
                     f'температура {data["main"]["temp"]}°C, '
                     f'ощущается как {data["main"]["feels_like"]}°C, '
                     f'влажность составляет {data["main"]["humidity"]}%.'
                     )


@bot.message_handler(commands=['weather'])
def get_weather_town(message):
    """
    Handles the /weather command from the user.

    Args:
        message (object): The user's message object.

    Returns:
        None
    """
    city = ' '.join(message.text.split()[1:])
    if not re.match(r'^[\w\s-]+$', city):
        bot.send_message(message.chat.id, 'Пожалуйста, введите корректное название города')
    else:
        data = get_city_cords(city)
        if type(data) == list:
            bot.send_message(message.chat.id, 'Было найдено несколько городов. Пожалуйста, выберите один из них.')
            msg = ''
            for i in data:
                count = i.split('. ', 1)[0]
                city_info = json.loads(i.split('. ', 1)[1])
                msg += f'{count}: {city_info["name"]} из {city_info["country"]} по координатам ({city_info["lat"]}, {city_info["lon"]})\n'
            bot.send_message(message.chat.id, msg.strip())
            bot.register_next_step_handler(message, select_town, data)
        elif type(data) == dict:
            get_weather_report(message, data)
        elif data == False:
            bot.send_message(message.chat.id, f'Город {city} не найден')


@bot.message_handler(commands=['start'])
def welcome_user(message):
    """
    Handles the /start command from the user and sends a welcome message.

    Args:
        message (object): The user's message object.

    Returns:
        None
    """
    if message.from_user.first_name:
        name = message.from_user.first_name
    elif message.from_user.last_name:
        name = message.from_user.last_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "пользователь"

    bot.send_message(message.chat.id,
                     f'Здравствуй, {name}!\n'
                     f'Я - бот, который поможет вам узнать погоду в нужном месте. Просто напишите мне /help :)')


@bot.message_handler(commands=['help'])
def get_functionality(message):
    """
    Handles the /help command from the user and sends a list of available bot functions.

    Args:
        message (object): The user's message object.

    Returns:
        None
    """
    bot.send_message(message.chat.id, f'Доступные функции:\n'
                                      f'/weather [Название города] - узнать погоду в городе\n'
                                      f'/help - функциональность бота')


bot.infinity_polling()
