from datetime import datetime, timedelta

from statsmodels.tsa.ar_model import AR

from airmon import const
from airmon.storage import get_co2_levels_series


def get_train_data():
    lookback_date = datetime.utcnow() - timedelta(seconds=const.train_time_secs)
    data = get_co2_levels_series(lookback_date)
    return data


def predict():
    data = get_train_data()
    prediction_time = datetime.utcnow() + timedelta(seconds=const.predict_time_secs)
    model = AR(data)
    model_fit = model.fit()
    # predictions = model_fit.predict(start=data_cnt, end=data_cnt + const.predict_points)
    predictions = model_fit.predict(end=prediction_time)
    return predictions
