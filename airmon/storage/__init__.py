from datetime import datetime

import pandas as pd
from pony import orm

from airmon.storage.models import CO2Level, Channel


def get_co2_levels(date_from):
    return orm.select(l for l in CO2Level if l.timestamp < date_from).order_by(CO2Level.timestamp)


def get_co2_levels_series(date_from):
    levels = ((l.timestamp, l.value) for l in get_co2_levels(date_from))
    timestamps, values = list(zip(*levels))
    return pd.Series(values, index=timestamps)


@orm.db_session
def store_co2_level(value, timestamp=None):
    return CO2Level(timestamp=timestamp or datetime.utcnow(), value=value)


@orm.db_session
def add_channel(chid):
    return Channel(chid=chid)


@orm.db_session
def remove_channel(chid):
    Channel.delete(chid=chid)


def get_channels():
    return orm.select(c for c in Channel)


def get_channels_id():
    return [c.chid for c in get_channels()]
