from keras.models import Sequential
from keras import layers
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import math


class TimeSeriesGenerator:
    def __init__(self, series: list) -> None:
        self.steps = max(4, math.ceil(len(series) * 0.1))
        self.model = Sequential(
            [
                layers.LSTM(32, input_shape=(self.steps, 1)),
                layers.Dense(8),
                layers.Dense(1),
            ]
        )
        self.scaler = MinMaxScaler()
        self.series = self.scaler.fit_transform(np.array(series).reshape(-1, 1))
        self.model.compile(loss="mse", optimizer="adam")
        self.train()

    def train_series_split(self, series):
        series = np.array(series)
        X_train = []
        y_train = []
        for i in range(self.steps, len(series)):
            X_train.append(series[i - self.steps : i])
            y_train.append(series[i])
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        return X_train, y_train

    def train(self):
        print("Training model...")
        x, y = self.train_series_split(self.series)
        batch_size = len(self.series) // 50 if len(self.series) > 50 else 1
        print("Batch size:", batch_size)
        self.model.fit(x, y, epochs=20, batch_size=batch_size, verbose=True)
        print("Model trained.")

    def predict(self):
        x_test = np.array(self.series[-self.steps :])
        predictions = []
        for i in range(self.steps):
            pred = self.model.predict(x_test.reshape(1, self.steps, 1))
            predictions.append(pred[0][0])
            x_test = np.append(x_test[1:], pred[0])

        return self.scaler.inverse_transform(
            np.array(predictions).reshape(-1, 1)
        ).reshape(-1)
