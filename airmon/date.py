from datetime import datetime, timedelta


def trim_secs(dt):
    return dt - timedelta(seconds=dt.second, microseconds=dt.microsecond)


def now():
    return trim_secs(datetime.utcnow())


def past(**kwargs):
    return now() - timedelta(**kwargs)


def future(**kwargs):
    return now() + timedelta(**kwargs)
