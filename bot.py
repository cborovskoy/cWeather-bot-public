from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import pyowm
from pyowm.utils.config import get_default_config

from settings import get_tg_token, get_owm_token

config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = pyowm.OWM(get_owm_token())
mgr = owm.weather_manager()


def message_handler(update: Update, context: CallbackContext):
    """
    Функция реагирования на сообщение
    """

    place = update.message.text

    try:
        weather = mgr.weather_at_place(place).weather
    except:
        reply_text = f'Города «{place}» нет в моей базе'
    else:
        temp_place = '{:+}'.format(int(weather.temperature("celsius")["temp"]))
        status_place = weather.detailed_status

        emoji_weather = {
            'облачно с прояснениями': '⛅',
            'ясно': '☀',
            'переменная облачность': '☁',
            'пасмурно': '☁',
            'небольшой дождь': '🌧️',
            'сильный дождь': '🌧️',
            'дождь': '🌧️',
            'плотный туман': '🌫️',
            'туман': '🌫️',
            'мгла': '🌫️',
            'небольшая облачность': '🌤️',
            'пыльная буря': '🌪️'

        }
        if status_place in emoji_weather:
            emoji = emoji_weather[status_place]
        else:
            emoji = ''

        reply_text = f'{emoji} {temp_place} | {status_place}\n\nВ городе {place}'

    update.message.reply_text(
        text=reply_text
    )


def main():
    """
    Основная функция бота.
    """

    updater = Updater(
        token=get_tg_token(), use_context=True
    )

    handler = MessageHandler(Filters.all, message_handler)
    updater.dispatcher.add_handler(handler)

    # Начать бесконечную обработку входящих сообщений
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
