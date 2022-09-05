import logging
import requests
from telegram.ext import Updater, CommandHandler, \
                            MessageHandler, Filters
import config



logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')



def greet_user(update, context):
    update.message.reply_text("Привет, введи имя города")

def show_weather(update, context):
    """ get weather data from openweather and send current weather to telegram """
    
    city_name = update.message.text.strip()    
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={config.WEATHER_TOKEN}&lang=ru&units=metric")
    
    if response.status_code == 404:
        update.message.reply_text(f"Город с именем {city_name} не найден")
        return
    
    json = response.json()
    answer = f"""
    Погода в {json['name']}:
    {json['weather'][0]['description']}, температура {json['main']['temp']} (по ощущениям {json['main']['feels_like']})
    """
    update.message.reply_text(answer)

def main():
    """ my first telegram bot """
    mybot = Updater(config.TELEGRAM_BOT_TOKEN)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, show_weather))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()