import os
import replicate
from utils.file_utils import unique_filename

replicate_client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))


def generate_video(prompt, path, scene_no):
    print(f"🎬 Generating video for scene {scene_no}")

    full_prompt = f"""
    {prompt},
    cinematic, realistic, smooth motion, 4k, highly detailed
    """

    try:
        output = replicate_client.run(
            "lucataco/animate-diff:latest",  # stable model
            input={
                "prompt": full_prompt,
                "num_frames": 16,
                "fps": 6
            }
        )

        video_url = output  # returns hosted URL

        # download video
        import requests
        res = requests.get(video_url)

        filename = f"scene_{scene_no}.mp4"
        file_path = os.path.join(path, filename)

        with open(file_path, "wb") as f:
            f.write(res.content)

        print(f"✅ Saved: {file_path}")

        return file_path

    except Exception as e:
        print("❌ Video error:", e)
        return None