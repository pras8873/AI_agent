import shutil
import os

def generate_video(image_path, scene_no, path):
    video_path = os.path.join(path, f"scene_{scene_no}.mp4")
    shutil.copy(image_path, video_path)
    return video_path
