'''import os
import requests
import base64
import time
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-image:generateContent?key={API_KEY}"


def generate_image(prompt, path, scene_no):
    print(f"\n🎨 Generating image for scene {scene_no}")
    character= CHARACTER = """
    25-year-old Indian male, short black hair, light beard, medium build,
    wearing blue t-shirt and jeans, same face, same person, consistent identity
    """
    full_prompt = f"""
    {character},{prompt},
    vertical 9:16 portrait for YouTube Shorts,
    full body framing,
    young Indian male,
    same style, similar face, same outfit,
    centered composition,
    cinematic lighting,
    ultra realistic,
    4k,
    sharp focus,
    professional photography
    """

    try:
        # small delay (safe)
        time.sleep(2)

        response = requests.post(
            URL,
            headers={"Content-Type": "application/json"},
            json={
                "contents": [
                    {
                        "parts": [
                            {"text": full_prompt}
                        ]
                    }
                ],
                "generationConfig": {
                    "response_mime_type": "image/png"
                }
            },
            timeout=60
        )

        response.raise_for_status()
        data = response.json()

        print("🔍 Gemini response received")

        # 🔥 Extract image (base64)
        image_data = data["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
        image_bytes = base64.b64decode(image_data)

        filename = f"scene_{scene_no}.png"
        file_path = os.path.join(path, filename)

        with open(file_path, "wb") as f:
            f.write(image_bytes)

        print(f"✅ Saved: {file_path}")
        return file_path

    except Exception as e:
        print("❌ Gemini Image Error:", e)
        return None'''

import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

def generate_image(prompt, path, scene_no):
    print(f"🎨 Generating Scene {scene_no}")
    print("📁 Path:", path)

    os.makedirs(path, exist_ok=True)

    # 🔥 STRONG CHARACTER LOCK
    character = """
    same person in all scenes,
    25-year-old Indian male,
    short black hair, light beard,
    medium build,
    wearing blue t-shirt and jeans,
    consistent face, consistent identity, same outfit
    """

    # 🔥 STRUCTURED PROMPT (VERY IMPORTANT)
    full_prompt = f"""
    {character}

    SCENE DESCRIPTION:
    {prompt}

    ACTION:
    actively performing physics experiment,
    hands interacting with objects,
    visible motion and engagement

    FOCUS:
    experiment clearly visible,
    physics concept visually explained,
    no close-up face shot,
    no portrait framing

    CAMERA:
    mid-shot or wide shot,
    subject + experiment both visible,
    not centered portrait

    STYLE:
    cinematic lighting,
    ultra realistic,
    high detail,
    9:16 vertical,
    YouTube Shorts style

    NEGATIVE:
    close-up face, selfie, portrait only, blurry, extra people, distorted face
    """

    url = "https://api.together.xyz/v1/images/generations"

    payload = {
        "model": "black-forest-labs/FLUX.1-schnell",
        "prompt": full_prompt,
        "width": 576,
        "height": 1024,
        "steps": 4,
        "n": 1
    }

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()["data"][0]
        filename = os.path.join(path, f"scene_{scene_no}.png")

        if "b64_json" in data:
            image_bytes = base64.b64decode(data["b64_json"])
            with open(filename, "wb") as f:
                f.write(image_bytes)

        elif "url" in data:
            img = requests.get(data["url"])
            with open(filename, "wb") as f:
                f.write(img.content)

        print(f"✅ Saved: {filename}")
        return filename

    else:
        print(f"❌ Error: {response.text}")
        return None
