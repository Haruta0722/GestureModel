import os, numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.utils import to_categorical

DATA_DIR = "keypoints_data"
X, y = [], []

for file in os.listdir(DATA_DIR):
    if file.endswith(".npy"):
        label_path = os.path.join(DATA_DIR, file.replace(".npy", ".label"))
        with open(label_path) as f:
            label = int(f.read())
        x = np.load(os.path.join(DATA_DIR, file))
        X.append(x)
        y.append(label)

X = np.array(X)
y = to_categorical(np.array(y), num_classes=100)

model = Sequential([
    LSTM(128, return_sequences=False, input_shape=(30, 63)),
    Dense(64, activation='relu'),
    Dense(100, activation='softmax')
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X, y, epochs=25, batch_size=16, validation_split=0.2)
model.save("sign_lstm_model.h5")