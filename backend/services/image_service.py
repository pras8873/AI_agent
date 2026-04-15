import os
import requests

def generate_image(prompt, path, scene_no):
    print(f"🎨 Generating image for scene {scene_no}")

    # Using free placeholder image API (for now)
    image_url = f"https://picsum.photos/seed/{scene_no}/1024/1792"

    response = requests.get(image_url)

    file_path = os.path.join(path, f"scene_{scene_no}.png")

    with open(file_path, "wb") as f:
        f.write(response.content)

    print(f"✅ Image saved: {file_path}")

    return file_path