import os, json, urllib.request

VIDEO_DIR = "wlasl_videos"
os.makedirs(VIDEO_DIR, exist_ok=True)

with open("WLASL_v0.3.json", "r") as f:
    data = json.load(f)

top_100 = sorted(data, key=lambda x: -len(x["instances"]))[:100]

for entry in top_100:
    for inst in entry["instances"]:
        url = inst["url"]
        video_id = inst["video_id"]
        out_path = os.path.join(VIDEO_DIR, f"{video_id}.mp4")
        if not os.path.exists(out_path):
            try:
                urllib.request.urlretrieve(url, out_path)
                print(f"✅ {video_id}")
            except:
                print(f"❌ {video_id}")