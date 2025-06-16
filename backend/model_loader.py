import numpy as np
from tensorflow.keras.models import load_model
from utils.extract_keypoints import extract_keypoints_from_video

model = load_model("model/sign_lstm_model_126d.h5")

def load_model_and_predict(video_path):
    keypoints = extract_keypoints_from_video(video_path)  # (30, 126)
    keypoints = np.expand_dims(keypoints, axis=0)         # (1, 30, 126)
    prediction = model.predict(keypoints)
    return np.argmax(prediction)
