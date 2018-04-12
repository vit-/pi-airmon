import time
from datetime import datetime, timedelta

from airmon import const
from airmon.forecast import predict


def is_forecast_level_warning():
    forecast = predict()
    predicted = forecast[-1]
    # if predicted
