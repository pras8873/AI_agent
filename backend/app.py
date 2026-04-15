import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import os
os.environ["SSL_CERT_FILE"] = ""
os.environ["REQUESTS_CA_BUNDLE"] = ""

from flask import Flask, request, jsonify
from flask_cors import CORS

from services.openai_service import generate_content
from services.image_service import generate_image
from services.video_service import generate_video
from utils.file_utils import create_topic_folder
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend is running 🚀"

@app.route("/generate", methods=["POST"])
def generate():
    topic = request.json["topic"]
    data = generate_content(topic)
    return jsonify(data)

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

if __name__ == "__main__":
    app.run(debug=True)
