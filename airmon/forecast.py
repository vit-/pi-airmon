from statsmodels.tsa.ar_model import AR

from airmon import const, date
from airmon.storage import get_co2_levels_series


def get_train_data():
    lookback_date = date.past(seconds=const.train_time_secs)
    data = get_co2_levels_series(lookback_date)
    return data


def predict():
    data = get_train_data()
    prediction_time = date.future(seconds=const.predict_time_secs)
    model = AR(data)
    model_fit = model.fit()
    predictions = model_fit.predict(end=prediction_time)
    return predictions
