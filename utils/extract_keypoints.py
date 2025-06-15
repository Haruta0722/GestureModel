import cv2
import mediapipe as mp
import numpy as np

def extract_keypoints_from_video(video_path, max_frames=30):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2)  # 両手に変更
    cap = cv2.VideoCapture(video_path)
    keypoints_seq = []

    while len(keypoints_seq) < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(image)

        # 両手のキーポイント初期化（21×3 × 2 = 126次元）
        keypoints = np.zeros(126)

        if result.multi_hand_landmarks:
            for idx, hand in enumerate(result.multi_hand_landmarks):
                if idx > 1:
                    break  # 最大2つまで
                hand_keypoints = np.array([[lm.x, lm.y, lm.z] for lm in hand.landmark]).flatten()
                keypoints[idx * 63:(idx + 1) * 63] = hand_keypoints  # 左右それぞれに格納

        keypoints_seq.append(keypoints)

    cap.release()

    # 足りないフレームをゼロ埋め
    while len(keypoints_seq) < max_frames:
        keypoints_seq.append(np.zeros(126))

    return np.array(keypoints_seq)