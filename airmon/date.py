from datetime import datetime, timedelta


def trim_micros(dt):
    return dt - timedelta(microseconds=dt.microsecond)


def now():
    return trim_micros(datetime.utcnow())


def past(**kwargs):
    return now() - timedelta(**kwargs)


def future(**kwargs):
    return now() + timedelta(**kwargs)
