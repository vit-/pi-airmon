import asyncio
import os
import time
from copy import copy

import aiotg
import matplotlib
matplotlib.use('Agg')  # noqa

from airmon import const, forecast, storage, chart, date
from airmon.storage.models import bind_db


BOT_TOKEN = os.environ.get('TG_BOT_TOKEN')
BOT_NAME = os.environ.get('TG_BOT_NAME')
assert all([BOT_TOKEN, BOT_NAME])

_LAST_ALERT = 0

bot = aiotg.Bot(api_token=BOT_TOKEN, name=BOT_NAME)


@bot.command(r'/start')
async def start(chat, match):
    storage.get_or_create_channel(chat.id)
    return await chat.reply('You\'ve been added to the notifications list')


@bot.command(r'/stop')
async def stop(chat, match):
    storage.remove_channel(chat.id)
    return await chat.reply('You\'ve been removed from the notifications list')


async def fire_alert(chat, img, severity):
    return await chat.send_photo(photo=img, caption='[%s] CO2 Alert!' % severity)


def render_image(predictions):
    lookback = date.past(hours=const.display_lookback_hours)
    data = storage.get_co2_levels_series(lookback)
    return chart.draw_png(data, predictions)


async def fire_alerts(predictions, severity):
    global _LAST_ALERT
    since_last_alert = time.time() - _LAST_ALERT
    if since_last_alert < const.alerts_cooldown_secs:
        return
    _LAST_ALERT = time.time()

    img = render_image(predictions)

    for chid in storage.get_channels_id():
        chat = bot.channel(chid)
        await fire_alert(chat, copy(img), severity)
    img.close()


@bot.command(r'/fire')
async def fire(chat, match):
    predictions = forecast.predict()
    img = render_image(predictions)
    return await fire_alert(chat, img, 'TEST')


async def monitor():

    while True:
        predictions = forecast.predict()
        val = predictions[-1]
        if val > const.co2_level_critical:
            await fire_alerts(predictions, 'CRITICAL')
        elif val > const.co2_level_warning:
            await fire_alerts(predictions, 'WARNING')
        await asyncio.sleep(const.monitor_interval_secs)


if __name__ == '__main__':
    print('Starting app')
    bind_db()
    loop = asyncio.get_event_loop()
    loop.call_soon(monitor)
    loop.run_until_complete(bot.loop())
