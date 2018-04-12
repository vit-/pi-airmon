from datetime import datetime

from pony import orm

db = orm.Database()


def bind_db(filename='storage.sqlite'):
    db.bind(provider='sqlite', filename=filename, created_db=True)
    db.generate_mapping(create_tables=True)


class CO2Level(db.Entity):
    timestamp = orm.Required(datetime)
    value = orm.Required(int)
