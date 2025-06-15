import numpy as np
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

DATA_DIR = "keypoints_data"
SEQUENCE_LENGTH = 30
FEATURE_SIZE = 126
NUM_CLASSES = 100

X = []
y = []

for fname in os.listdir(DATA_DIR):
    if fname.endswith(".npy"):
        landmark = np.load(os.path.join(DATA_DIR, fname))
        with open(os.path.join(DATA_DIR, fname.replace(".npy", ".label")), "r") as f:
            label = int(f.read())
        X.append(landmark)
        y.append(label)

X = np.array(X)  # shape: [samples, 30, 126]
y = to_categorical(y, NUM_CLASSES)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = Sequential([
    LSTM(128, return_sequences=True, input_shape=(SEQUENCE_LENGTH, FEATURE_SIZE)),
    Dropout(0.4),
    LSTM(64),
    Dropout(0.3),
    Dense(64, activation="relu"),
    Dense(NUM_CLASSES, activation="softmax")
])

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
model.summary()

model.fit(X_train, y_train, epochs=30, batch_size=32, validation_data=(X_test, y_test))

model.save("sign_lstm_model_126d.h5")