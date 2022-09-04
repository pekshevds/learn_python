import logging
import requests
import json

from telegram.ext import Updater, CommandHandler, \
                            MessageHandler, Filters

from readme import telegram_bot_password, wether_token



logging.basicConfig(filename='bot.log', level=logging.INFO)



def greet_user(update, context):
    print("called /start")
    update.message.reply_text("Hello user")

def show_wether(update, context):
    """ get wether data from openwether and send current wether to telegram """
    text = update.message.text
    city_name = text
    country_code = "+7"
    API_key = wether_token
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}&lang=ru&units=metric"
    response = requests.get(url)
    if response.status_code == 404:
        update.message.reply_text(f"City {city_name} not found")
        return

    my_data = json.loads(response.text)
    
    result = f"""
    Погода в {my_data['name']}:
    {my_data['weather'][0]['description']}, температура {my_data['main']['temp']} (по ощущениям {my_data['main']['feels_like']})
    """

    update.message.reply_text(result)

def main():
    """ my first telegram bot """
    mybot = Updater(telegram_bot_password)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, show_wether))

    logging.info("bot started")

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()