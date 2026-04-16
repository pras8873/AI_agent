'''import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "image/png"
}


def generate_image(prompt, path, scene_no):
    print(f"🎨 Generating image for scene {scene_no}")

    # 🔥 Improve prompt automatically
    full_prompt = f"""
        {prompt},
        young Indian person,
        consistent character,
        cinematic lighting,
        depth of field,
        highly detailed,
        4k,
        ultra realistic
        """

    for _ in range(3):
        response = requests.post(
            API_URL,
            headers=headers,
            json={
            "inputs": full_prompt,
            "options": {"wait_for_model": True}
            },
            timeout=120
        )
        if response.status_code == 200:
            break

    if response.status_code != 200:
        print("❌ HF Error:", response.text)
        return None

    filename = f"scene_{scene_no}.png"
    file_path = os.path.join(path, filename)

    with open(file_path, "wb") as f:
        f.write(response.content)

    print(f"✅ Image saved: {file_path}")

    return file_path'''

import os
import requests
import base64

AIPIPE_URL = "https://aipipe.org/geminiv1beta/models/gemini-2.5-flash-image-preview:generateContent"


def generate_image(prompt, path, scene_no, token):
    print(f"🎨 Generating image for scene {scene_no}")

    response = requests.post(
        AIPIPE_URL,
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": token
        },
        json={
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        },
        timeout=60
    )

    if response.status_code != 200:
        print("❌ Gemini Error:", response.text)
        return None

    data = response.json()

    try:
        base64_img = data["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]

        image_bytes = base64.b64decode(base64_img)

        filename = f"scene_{scene_no}.png"
        file_path = os.path.join(path, filename)

        with open(file_path, "wb") as f:
            f.write(image_bytes)

        print(f"✅ Saved: {file_path}")

        return file_path

    except Exception as e:
        print("❌ Parsing error:", e)
        return None