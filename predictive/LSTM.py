import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler


class ModelBuilder:
    def __init__(self, model_path, input_data, epochs=100, ):
        self.scaler = None
        self.batch_size = 32
        self.epochs = epochs
        self.loss = 'mean_squared_error'
        self.optimizer = 'adam'
        self.sequence_length = 32
        self.model_path = model_path
        self.train_split_percentage = 0.8
        self.data = input_data

    def preprocessing_data(self, data):
        data = np.array(data)
        data = data.reshape(-1, 1)

        # self.scaler = MinMaxScaler(feature_range=(0, 1))
        # normalised_data = self.scaler.fit_transform(data)

        normalised_data = data
        normalised_data = np.array(normalised_data)
        normalised_data = normalised_data.reshape(-1, 1)
        print(f"reshape data and {normalised_data.shape} {normalised_data}")
        X, y = [], []
        for i in range(len(normalised_data) - self.sequence_length):
            X.append(normalised_data[i:(i + self.sequence_length)])
            y.append(normalised_data[i + self.sequence_length])
        print("Preprocessing completed")
        return np.array(X), np.array(y)

    def create_model(self, X, y):
        model = Sequential()
        model.add(LSTM(50, activation='relu', input_shape=(self.sequence_length, 1)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mean_squared_error')

        # Summary of the model
        model.summary()

        # model.compile(optimizer=self.optimizer, loss=self.loss)
        model.fit(X, y, epochs=self.epochs)
        # model.fit(X_train, y_train, epochs=self.epochs, batch_size=self.batch_size , validation_data=(X_test, y_test))
        model.save(f'{self.model_path}.h5')
        self.predict(self.data[-self.sequence_length:])

    def predict(self, prediction_data):
        print(f'Raw {prediction_data}')
        model = load_model(f'{self.model_path}.h5')
        input_data = np.array(prediction_data).reshape((1, self.sequence_length, 1))
        print(input_data)
        predicted = model.predict(input_data)
        # p_data = self.scaler.inverse_transform(predicted)
        print(predicted)

    def build_model(self):
        X, y = self.preprocessing_data(self.data)
        self.create_model(X, y)


if __name__ == '__main__':

    data = [i for i in range(112)]
    pre = [i for i in range(80, 112)]
    # ModelBuilder('last_dance', data, 100).build_model()
    LSTM_B = ModelBuilder('last_dance', data, 200)

    LSTM_B.build_model()
    LSTM_B.predict(pre)
