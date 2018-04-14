from datetime import datetime, timedelta


def past(**kwargs):
    return datetime.utcnow() - timedelta(**kwargs)


def future(**kwargs):
    return datetime.utcnow() + timedelta(**kwargs)
