from aiogram import Router, F
from aiogram.types import Message
import pyowm
from pyowm.commons.exceptions import NotFoundError
from pyowm.utils.config import get_default_config

from src.config import load_config

router = Router()


@router.message(~F.text.startswith('/'))
async def msg_handler(message: Message):
    config_dict = get_default_config()
    config_dict['language'] = 'ru'
    config = load_config()
    owm = pyowm.OWM(config.owm_token)
    mgr = owm.weather_manager()

    place = message.text

    try:
        weather = mgr.weather_at_place(place).weather
    except NotFoundError:
        reply_text = f'Города «{place}» нет в моей базе'
    else:
        temp_place = '{:+}'.format(int(weather.temperature("celsius")["temp"]))
        status_place = weather.detailed_status

        emoji_weather = {'облачно с прояснениями': '⛅',
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

        emoji = emoji_weather[status_place] if status_place in emoji_weather else ''
        reply_text = f'{emoji} {temp_place} | {status_place}\n\nВ городе {place}'

    await message.answer(text=reply_text)
