import numpy as np

def generate_ndvi_series():
    return np.random.uniform(0.3, 0.8, 10)

def detect_trend(series):
    trend = series[-1] - series[0]

    if trend < -0.1:
        return "Decreasing (Risk)"
    elif trend > 0.1:
        return "Increasing (Healthy)"
    else:
        return "Stable"