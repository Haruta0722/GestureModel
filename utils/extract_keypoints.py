import cv2
import mediapipe as mp
import numpy as np

def extract_keypoints_from_video(video_path, max_frames=30):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
    cap = cv2.VideoCapture(video_path)
    keypoints_seq = []

    while len(keypoints_seq) < max_frames:
        ret, frame = cap.read()
        if not ret: break
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(image)

        keypoints = np.zeros(21 * 3)
        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]
            keypoints = np.array([[lm.x, lm.y, lm.z] for lm in hand.landmark]).flatten()

        keypoints_seq.append(keypoints)

    cap.release()
    while len(keypoints_seq) < max_frames:
        keypoints_seq.append(np.zeros(21 * 3))

    return np.array(keypoints_seq)