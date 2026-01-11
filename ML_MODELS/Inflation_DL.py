import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, LSTM, Dense

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "Inflation_Data.csv")

_model = None
_scaler = None


def _train_inflation_model():
    global _model, _scaler

    df = pd.read_csv(DATA_PATH)
    df = df.sort_values("Year")

    _scaler = MinMaxScaler()
    scaled = _scaler.fit_transform(df[['GDP_Growth', 'Inflation']])

    def create_sequences(data, window_size=10):
        X, y = [], []
        for i in range(len(data) - window_size - 10):
            X.append(data[i:i + window_size])
            y.append(np.mean(data[i + window_size:i + window_size + 10, 1]))
        return np.array(X), np.array(y)

    X, y = create_sequences(scaled)

    model = Sequential([
        Input(shape=(X.shape[1], X.shape[2])),
        LSTM(64),
        Dense(32, activation='relu'),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=50, batch_size=16, verbose=0)

    _model = model


def predict_inflation_rate():
    """
    Returns predicted inflation as decimal
    Example: 0.0645 = 6.45%
    """

    global _model, _scaler

    if _model is None:
        _train_inflation_model()

    df = pd.read_csv(DATA_PATH)
    df = df.sort_values("Year")

    scaled = _scaler.transform(df[['GDP_Growth', 'Inflation']])

    last_10 = scaled[-10:].reshape((1, 10, 2))
    pred_scaled = _model.predict(last_10, verbose=0)[0][0]

    inflation_min = _scaler.data_min_[1]
    inflation_max = _scaler.data_max_[1]

    predicted_inflation = pred_scaled * (inflation_max - inflation_min) + inflation_min

    return round(predicted_inflation / 100, 4)



