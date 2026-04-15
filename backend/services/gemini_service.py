import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AIPIPE_API_KEY")

URL = "https://aipipe.org/openai/v1/chat/completions"


def generate_content(topic):
    prompt = f"""
You are a professional YouTube Shorts script creator.

Create a HIGHLY engaging short-form video content package for the topic: "{topic}"

⚠️ STRICT RULES (MUST FOLLOW):
- Output ONLY valid JSON
- DO NOT add explanation
- DO NOT add markdown
- MUST generate EXACTLY 12 scenes
- Each scene MUST be unique and detailed
- Maintain SAME CHARACTER (young Indian male/female) in ALL scenes

JSON FORMAT (STRICT):
{{
  "topic": "",
  "video_title": "",
  "description": "",
  "tags": [],
  "script_50_sec": "",
  "scenes": [
    {{
      "scene_no": 1,
      "scene_title": "",
      "image_prompt": "",
      "animation_prompt": ""
    }}
  ]
}}

CONTENT RULES:
- Script: Hinglish, viral style, hook + explanation + CTA
- Tone: energetic, relatable, slightly dramatic
- Tags: at least 10 SEO keywords
- Description: engaging + searchable

IMAGE PROMPT RULES:
- MUST include: portrait, young Indian character, cinematic lighting, attractive background, realistic, 4K
- Add specific action per scene

ANIMATION RULES:
- EXACT format: "4-second animation: ..."
- Describe motion clearly

⚠️ VERY IMPORTANT:
- Scenes count MUST be exactly 10
- If not 10 → response is INVALID
- Ensure full JSON completeness
"""

    try:
        response = requests.post(
            URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            },
            timeout=30
        )

        print("STATUS:", response.status_code)
        print("RAW:", response.text)

        response.raise_for_status()
        data = response.json()

        text = data["choices"][0]["message"]["content"]

        # Clean JSON
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]

        start = text.find("{")
        end = text.rfind("}") + 1
        text = text[start:end]

        return json.loads(text)

    except Exception as e:
        print("❌ Error:", e)
        return {"error": "AI Pipe failed"}