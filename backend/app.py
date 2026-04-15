import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import os
os.environ["SSL_CERT_FILE"] = ""
os.environ["REQUESTS_CA_BUNDLE"] = ""
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS

from services.gemini_service import generate_content
from services.image_service import generate_image
from services.video_service import generate_video
from services.voice_service import generate_voice
from utils.file_utils import create_topic_folder
from dotenv import load_dotenv
load_dotenv()

app = Flask(
    __name__,
    static_folder="../frontend",
    static_url_path=""
)

CORS(app)

@app.route("/")
def home():
    return send_from_directory("../frontend", "index.html")

@app.route("/generate", methods=["POST"])
def generate():
    print("🔥 /generate endpoint hit")

    data = request.json
    print("📥 Incoming data:", data)

    topic = data.get("topic")
    print("📌 Topic:", topic)

    result = generate_content(topic)

    print("✅ Sending response")

    return jsonify(result)

@app.route("/process", methods=["POST"])
def process():
    data = request.json
    topic = data["topic"]

    folder = create_topic_folder(topic)
    results = []

    for scene in data["scenes"]:
        scene_no = scene["scene_no"]

        img = generate_image(scene["image_prompt"], folder, scene_no)
        vid = generate_video(img, scene_no, folder)

        results.append({
            "scene": scene_no,
            "image": img,
            "video": vid
        })

    return jsonify({
        "status": "completed",
        "output_folder": folder,
        "files": results
    })

import subprocess

def merge_audio(video_path, audio_path, output_path):
    command = [
        "ffmpeg",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        "-y",
        output_path
    ]

    subprocess.run(command)

if __name__ == "__main__":
    app.run(debug=True)
