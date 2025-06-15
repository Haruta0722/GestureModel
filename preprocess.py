import os, json, numpy as np
from utils.extract_keypoints import extract_keypoints_from_video

VIDEO_DIR = "wlasl_videos"
OUT_DIR = "keypoints_data"
os.makedirs(OUT_DIR, exist_ok=True)

with open("WLASL_v0.3.json", "r") as f:
    data = json.load(f)

top_100 = sorted(data, key=lambda x: -len(x["instances"]))[:100]
label_map = {entry["gloss"]: i for i, entry in enumerate(top_100)}

for entry in top_100:
    label = entry["gloss"]
    label_id = label_map[label]

    for inst in entry["instances"]:
        vid = inst["video_id"]
        path = os.path.join(VIDEO_DIR, f"{vid}.mp4")
        if not os.path.exists(path): continue
        try:
            x = extract_keypoints_from_video(path)
            np.save(os.path.join(OUT_DIR, f"{vid}.npy"), x)
            with open(os.path.join(OUT_DIR, f"{vid}.label"), "w") as f:
                f.write(str(label_id))
        except Exception as e:
            print(f"Error: {vid} - {e}")