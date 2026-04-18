import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AIPIPE_API_KEY")

URL = "https://aipipe.org/openai/v1/chat/completions"


def generate_content(topic):
    prompt = f"""
You are an expert viral YouTube Shorts creator + AI visual prompt engineer.

Create a COMPLETE high-quality content package for: "{topic}"

⚠️ STRICT OUTPUT RULES:
- ONLY valid JSON
- NO markdown
- NO explanation
- EXACTLY 10 scenes (NOT 12)
- Same character in ALL scenes

CHARACTER:
- 25-year-old Indian male
- short black hair, light beard
- blue t-shirt, jeans
- SAME face, SAME outfit, SAME person

JSON FORMAT:
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

🔥 SCRIPT RULES:
- Hinglish
- Strong hook in first line
- Curiosity + surprise
- Simple explanation
- End with CTA

🔥 IMAGE PROMPT RULES (VERY STRICT):
Each image_prompt MUST include:

1. CLEAR ACTION (what character is doing)
2. PHYSICS EXPERIMENT visible
3. HAND INTERACTION (must)
4. ENVIRONMENT (room/lab/home etc.)
5. VISUAL EFFECT (spark, motion, energy, etc.)

⚠️ MUST AVOID:
- portrait
- close-up face
- standing idle
- posing

✅ MUST INCLUDE:
- "mid shot"
- "hands interacting"
- "experiment clearly visible"
- "dynamic action"

🔥 ANIMATION RULES:
Format EXACTLY:
"4-second animation: [camera movement + subject motion + effect]"

Example:
"4-second animation: slight zoom-in, hand touches metal, small electric spark appears"

🔥 SCENE QUALITY:
- Each scene must be visually DIFFERENT
- Show progression of concept
- Not repetitive

🔥 TAGS:
- Minimum 12
- SEO optimized

🔥 DESCRIPTION:
- Engaging + searchable

⚠️ FINAL CHECK:
- Exactly 10 scenes
- All scenes have detailed prompts
- JSON must be valid
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