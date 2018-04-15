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


async def help_msg(chat):
    msg = """
        /subscribe - be alerted if forecast goes bad
        /unsubscribe - stop receiving alerts
        /stats3 - renders chart for last 3 hours
        /stats6 - renders chart for last 6 hours
        /stats12 - renders chart for last 12 hours
        /stats24 - renders chart for last 24 hours
    """
    return await chat.send(msg)


@bot.command(r'/help')
async def help_(chat, match):
    return await help_msg(chat)


@bot.command(r'/start')
async def start(chat, match):
    return await help_msg(chat)


@bot.command(r'/subscribe')
async def subscribe(chat, match):
    storage.get_or_create_channel(chat.id)
    return await chat.reply('You\'ve been added to the notifications list')


async def unsubscribe(chat):
    storage.remove_channel(chat.id)
    return await chat.reply('You\'ve been removed from the notifications list')


@bot.command(r'/unsubscribe')
async def unsubscribe_(chat, match):
    return await unsubscribe(chat)


@bot.command(r'/stop')
async def stop(chat, match):
    return await unsubscribe(chat)


def render_message(data, predictions=None, severity=None):
    msg = ''
    if severity:
        msg += '[%s] CO2 Alert!\n' % severity
    msg += 'Current level: %s\n' % data[-1]
    if predictions:
        msg += 'Upcoming level: %s' % predictions[-1]
    return msg


@bot.command(r'/stats(\d+)')
async def stats(chat, match):
    hours = int(match.groups()[0])
    lookback = date.past(hours=hours)
    data = storage.get_co2_levels_series(lookback)
    img = chart.draw_png(data)
    msg = render_message(data)
    return await chat.send_photo(photo=img, caption=msg)


async def fire_alerts(predictions, severity):
    global _LAST_ALERT
    since_last_alert = time.time() - _LAST_ALERT
    if since_last_alert < const.alert_cooldown_secs:
        return
    _LAST_ALERT = time.time()

    lookback = date.past(hours=lookback_hours)
    data = storage.get_co2_levels_series(lookback)
    img = chart.draw_png(data, predictions)
    msg = render_message(data, predictions, severity)

    for chid in storage.get_channels_id():
        chat = bot.channel(chid)
        await chat.send_photo(photo=img, caption=msg)
    img.close()


async def monitor():
    print('Starting monitoring')
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
