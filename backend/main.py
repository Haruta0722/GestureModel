from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import tensorflow as tf
import os, json

# モデルファイルのパス
MODEL_PATH = os.path.join("model", "sign_lstm_model_126d.h5")

# モデル読み込み
model = tf.keras.models.load_model(MODEL_PATH)

with open("WLASL_v0.3.json", "r") as f:
    data = json.load(f)

top_100 = sorted(data, key=lambda x: -len(x["instances"]))[:100]
label_names = [entry["gloss"] for entry in top_100]

SEQUENCE_LENGTH = 30
FEATURE_SIZE = 126

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.jsの開発用ポート
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# リクエストのデータ構造定義
class KeypointSequence(BaseModel):
    sequence: list[list[float]]  # 30 x 126 の配列（フレーム x 特徴量）

@app.post("/predict")
def predict_sign(data: KeypointSequence):
    # 入力検証
    if len(data.sequence) != SEQUENCE_LENGTH:
        raise HTTPException(status_code=400, detail="Invalid sequence length")

    input_data = np.array(data.sequence).reshape(1, SEQUENCE_LENGTH, FEATURE_SIZE)

    # 推論
    prediction = model.predict(input_data)[0]
    predicted_class = int(np.argmax(prediction))
    confidence = float(np.max(prediction))

    return {
        "label": label_names[predicted_class],
        "confidence": confidence
    }