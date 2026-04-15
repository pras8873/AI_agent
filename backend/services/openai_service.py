import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import httpx

load_dotenv()

# Create custom HTTP client (disable SSL verification)
http_client = httpx.Client(verify=False)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    http_client=http_client
)
def generate_content(topic):
    prompt = f"""
Create a short-form video content package for the topic: "{topic}"

Return ONLY valid JSON (no extra text).
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    content = response.choices[0].message.content
    return json.loads(content)
