from openai import OpenAI
import base64
import os
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_image(prompt, path, scene_no):
    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1792"
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    file_path = os.path.join(path, f"scene_{scene_no}.png")

    with open(file_path, "wb") as f:
        f.write(image_bytes)

    return file_path
