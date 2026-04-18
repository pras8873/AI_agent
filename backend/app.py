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

from services.image_service import generate_image
from utils.file_utils import create_topic_folder
import os

@app.route("/process", methods=["POST"])
def process():
    print("🎬 /process endpoint hit")

    data = request.json
    topic = data.get("topic", "default")

    print("📌 Topic:", topic)

    folder = create_topic_folder(topic)

    # Create images folder
    images_path = os.path.join(folder, "images")
    os.makedirs(images_path, exist_ok=True)

    scenes = data.get("scenes", [])

    generated_files = []

    for scene in scenes:
        scene_no = scene.get("scene_no")
        prompt = scene.get("image_prompt")

        print(f"🎨 Scene {scene_no}: {prompt}")

        img_path = generate_image(prompt, images_path, scene_no)

        generated_files.append(img_path)

    return {
        "status": "success",
        "images": generated_files
    }

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

from services.image_service import generate_image
import os

@app.route("/process-images", methods=["POST"])
def process_images():
    print("🎬 Processing images")

    data = request.json
    topic = data.get("topic", "default")

    folder = os.path.join("output", topic.replace(" ", "_"), "images")
    os.makedirs(folder, exist_ok=True)

    images = []

    import time

    for scene in data.get("scenes", []):
        img_path = generate_image(
            scene["image_prompt"],
            folder,
            scene["scene_no"]
        )

        if img_path:
            images.append(img_path)

        # 🔥 WAIT to avoid rate limit
        time.sleep(5)

    return {
        "status": "success",
        "images": images
    }

@app.route('/output/<path:filename>')
def serve_image(filename):
    return send_from_directory('output', filename)
from services.video_service import generate_video

@app.route("/generate-video", methods=["POST"])
def generate_video_route():
    print("🎬 Video generation started")

    data = request.json
    topic = data.get("topic", "default")

    folder = os.path.join("output", topic.replace(" ", "_"), "videos")
    os.makedirs(folder, exist_ok=True)

    videos = []

    for scene in data.get("scenes", []):
        video_path = generate_video(
            scene["animation_prompt"],
            folder,
            scene["scene_no"]
        )

        if video_path:
            videos.append(video_path)

    return {
        "status": "success",
        "videos": videos
    }
from flask import send_from_directory
@app.route('/output/<path:filename>')
def serve_file(filename):
    return send_from_directory('output', filename)

from flask import send_from_directory

@app.route('/output/<path:filename>')
def serve_output(filename):
    return send_from_directory('output', filename)


from flask import send_from_directory
import os

@app.route('/download-image/<path:filename>')
def download_image(filename):
    return send_from_directory(
        directory="output",
        path=filename,
        as_attachment=True   # 🔥 THIS FORCES DOWNLOAD
    )

@app.route('/generate-audio', methods=['POST'])
def generate_audio():
    data = request.json

    print("FULL DATA:", data)

    script = data.get("script")

    print("🎙 Script:", script)

    path = generate_voice(script)

    return {"audio_url": "/output/audio.wav"}

@app.route('/download-audio')
def download_audio():
    return send_from_directory(
        "output",
        "audio.wav",
        as_attachment=True
    )
if __name__ == "__main__":
    app.run(debug=True)
