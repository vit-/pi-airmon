from statsmodels.tsa.ar_model import AR

from airmon import const, date
from airmon.storage import get_co2_levels_series


def resample(data):
    data = data.resample('%ss' % const.sampling_interval_secs).mean()  # resample
    data = data.interpolate()  # remove NaN values
    return data


def get_train_data():
    lookback_date = date.past(minutes=const.train_time_mins)
    data = get_co2_levels_series(lookback_date)
    return resample(data)


def predict():
    data = get_train_data()
    model = AR(data)
    model_fit = model.fit()

    prediction_time = date.future(minutes=const.predict_time_mins)
    predictions = model_fit.predict(end=prediction_time)
    return predictions
