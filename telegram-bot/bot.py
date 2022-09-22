import logging
import requests
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, \
                            MessageHandler, Filters
import config


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


def greet_user(update, context):

    my_keyboard = ReplyKeyboardMarkup([['Погода в белгороде']])

    update.message.reply_text(
        "Привет, введи имя города",
        reply_markup=my_keyboard
        )

def get_city_weather(city_name):
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={config.WEATHER_TOKEN}&lang=ru&units=metric")
    if response.ok:
        return response.json()
    return False

def show_weather_in_belgorod(update, context):
    """ get weather data from openweather and send current weather to telegram """
                
    city_name = 'belgorod'
    city_weather = get_city_weather(city_name=city_name)
    if city_weather:
        answer = f"""
        Погода в {city_weather['name']}:
        {city_weather['weather'][0]['description']}, температура {city_weather['main']['temp']} (по ощущениям {city_weather['main']['feels_like']})
        """
    else:
        answer = f"Город с именем {city_name} не найден"    
    update.message.reply_text(answer)

def show_weather(update, context):
    """ get weather data from openweather and send current weather to telegram """
    
    city_name = update.message.text.strip()    
        
    city_weather = get_city_weather(city_name=city_name)
    if city_weather:
        answer = f"""
        Погода в {city_weather['name']}:
        {city_weather['weather'][0]['description']}, температура {city_weather['main']['temp']} (по ощущениям {city_weather['main']['feels_like']})
        """
    else:
        answer = f"Город с именем {city_name} не найден"    
    update.message.reply_text(answer)

def main():
    """ my first telegram bot """
    mybot = Updater(config.TELEGRAM_BOT_TOKEN)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.regex('^(Погода в белгороде)$'), show_weather_in_belgorod))
    dp.add_handler(MessageHandler(Filters.text, show_weather))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()