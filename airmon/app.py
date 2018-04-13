import asyncio
import os
import time
from datetime import datetime, timedelta

import aiotg

from airmon import const
from airmon.forecast import predict
from airmon.storage import get_co2_levels_series, get_or_create_channel, remove_channel, get_channels_id
from airmon.chart import draw_png


BOT_TOKEN = os.environ.get('TG_BOT_TOKEN')
BOT_NAME = os.environ.get('TG_BOT_NAME')
assert all([BOT_TOKEN, BOT_NAME])

_LAST_ALERT = 0

bot = aiotg.Bot(api_token=BOT_TOKEN, name=BOT_NAME)


@bot.command(r'/start')
async def start(chat, match):
    get_or_create_channel(chat.id)
    return await chat.reply('You\'ve been added to the notifications list')


@bot.command(r'/stop')
async def stop(chat, match):
    remove_channel(chat.id)
    return await chat.reply('You\'ve been removed from the notifications list')


async def fire_alert(chat, img, severity):
    return await chat.send_photo(photo=img, caption='[%s] CO2 Alert!' % severity)


async def fire_alerts(predictions, severity):
    global _LAST_ALERT
    since_last_alert = time.time() - _LAST_ALERT
    if since_last_alert < const.alerts_cooldown_secs:
        return
    _LAST_ALERT = time.time()

    lookback = datetime.utcnow() - timedelta(hours=const.display_lookback_hours)
    data = get_co2_levels_series(lookback)
    img = draw_png(data, predictions)

    for chid in get_channels_id:
        chat = bot.channel(chid)
        await fire_alert(chat, img, severity)


async def monitor():

    while True:
        predictions = predict()
        val = predictions[-1]
        if val > const.co2_level_critical:
            await fire_alerts(predictions, 'CRITICAL')
        elif val > const.co2_level_warning:
            await fire_alerts(predictions, 'WARNING')
        await asyncio.sleep(const.monitor_interval_secs)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.call_soon(monitor)
    loop.run_until_complete(bot.loop())
