import os
import requests
import base64
from dotenv import load_dotenv
from utils.file_utils import unique_filename

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

URL = f"https://texttospeech.googleapis.com/v1beta1/text:synthesize?key={API_KEY}"


def generate_voice(text, path):
    print("🎤 Generating Gemini voice...")

    payload = {
        "audioConfig": {
            "audioEncoding": "MP3",
            "pitch": 0,
            "speakingRate": 1
        },
        "input": {
            "prompt": "Read aloud in curious and slightly dramatic tone.",
            "text": text
        },
        "voice": {
            "languageCode": "en-IN",
            "modelName": "gemini-2.5-flash-tts",
            "name": "Charon"
        }
    }

    response = requests.post(
        URL,
        headers={"Content-Type": "application/json"},
        json=payload
    )

    data = response.json()

    print("🔍 Voice response:", data)

    try:
        audio_base64 = data["audioContent"]
        audio_bytes = base64.b64decode(audio_base64)

        filename = unique_filename("voice", "mp3")
        file_path = os.path.join(path, filename)

        with open(file_path, "wb") as f:
            f.write(audio_bytes)

        print(f"✅ Voice saved: {file_path}")

        return file_path

    except Exception as e:
        print("❌ Voice error:", e)
        return None