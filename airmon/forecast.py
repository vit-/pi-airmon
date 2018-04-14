from statsmodels.tsa.ar_model import AR

from airmon import const, date
from airmon.storage import get_co2_levels_series


def resample(data):
    return data.resample('%ss' % const.sampling_interval_secs).mean()


def get_train_data():
    lookback_date = date.past(seconds=const.train_time_secs)
    data = get_co2_levels_series(lookback_date)
    return resample(data)


def predict():
    data = get_train_data()
    model = AR(data)
    model_fit = model.fit()

    prediction_time = date.future(seconds=const.predict_time_secs)
    predictions = model_fit.predict(end=prediction_time)
    return predictions
