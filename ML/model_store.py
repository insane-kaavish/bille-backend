import pandas as pd
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from keras.layers import LSTM, Dense
from keras.models import Sequential
import pickle

# import data from csv file
df = pd.read_csv('Augmented_Model_Data.csv')

X = df.iloc[:, :-1]  # All columns except the last one
y = df.iloc[:, -1]   # The last column


# Preparing separate scalers for input features and target variable
scaler_X = MinMaxScaler(feature_range=(0, 1))
scaler_y = MinMaxScaler(feature_range=(0, 1))

# Scaling the features
scaled_X = scaler_X.fit_transform(X)
scaled_y = scaler_y.fit_transform(y.values.reshape(-1, 1))

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(scaled_X, scaled_y, test_size=0.2, random_state=42)

# Reshaping for LSTM: [samples, time steps, features]
X_train_reshaped = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
X_test_reshaped = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

# Building the LSTM model
model = Sequential()
model.add(LSTM(units=25, return_sequences=True, input_shape=(1, X_train.shape[1]))) # reduced the number of units from 50 to 25
model.add(LSTM(units=25))
model.add(Dense(1))

# Compiling the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Training the model
model.fit(X_train_reshaped, y_train, epochs=100, batch_size=32)

# Making predictions
y_pred_lstm = model.predict(X_test_reshaped)

# Rescale predictions back to original scale
y_pred_lstm_rescaled = scaler_y.inverse_transform(y_pred_lstm)


# save the model to disk
model_filename = 'model.sav'
pickle.dump(model, open(model_filename, 'wb'))