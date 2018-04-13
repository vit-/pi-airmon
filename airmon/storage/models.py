from datetime import datetime

from pony import orm

db = orm.Database()


def bind_db(filename='storage.sqlite'):
    db.bind(provider='sqlite', filename=filename, create_db=True)
    db.generate_mapping(create_tables=True)


class CO2Level(db.Entity):
    timestamp = orm.Required(datetime, unique=True)
    value = orm.Required(int)


class Channel(db.Entity):
    chid = orm.Required(str, unique=True)
