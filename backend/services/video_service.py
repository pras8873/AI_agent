import os
import shutil

def generate_video(image_path, scene_no, path):
    print(f"🎬 Generating video for scene {scene_no}")

    video_path = os.path.join(path, f"scene_{scene_no}.mp4")

    # TEMP: copy image as fake video
    shutil.copy(image_path, video_path)

    print(f"✅ Video saved: {video_path}")

    return video_path