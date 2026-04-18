const API = window.location.origin;

// 🔥 Generate JSON (script)
async function generate() {
  console.log("🔥 Generate button clicked");

  const topic = document.getElementById("topic").value;
  console.log("📌 Topic:", topic);

  try {
    const res = await fetch(`${API}/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic })
    });

    console.log("📡 Request sent");

    const data = await res.json();
    console.log("✅ Response received:", data);

    document.getElementById("jsonBox").value =
      JSON.stringify(data, null, 2);

  } catch (err) {
    console.error("❌ Error:", err);
    alert("Error occurred. Check console.");
  }
}


// 🔥 (optional) image processing if you still use it
async function process() {
  const jsonData = JSON.parse(
    document.getElementById("jsonBox").value
  );

  await fetch(`${API}/process`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(jsonData)
  });

  alert("Done!");
}


// 🎬 Generate video from scenes
async function createVideo() {
  console.log("🎬 Create Video clicked");

  const jsonText = document.getElementById("jsonBox").value;
  let data;

  try {
    data = JSON.parse(jsonText);
  } catch {
    alert("Invalid JSON!");
    return;
  }

  try {
    const res = await fetch(`${API}/generate-video`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const result = await res.json();

    console.log("🎬 Videos:", result);

    displayVideos(result.videos);

  } catch (err) {
    console.error("❌ Video error:", err);
    alert("Video generation failed");
  }
}


// 🎬 Display videos
function displayVideos(videos) {
  const container = document.getElementById("videoContainer");
  container.innerHTML = "";

  videos.forEach((videoPath) => {
    const video = document.createElement("video");
    video.src = videoPath;
    video.controls = true;
    video.style.width = "250px";
    video.style.margin = "10px";

    container.appendChild(video);
  });
}


// 🖼️ Display images (if needed)
function displayImages(images) {
  const container = document.getElementById("imageContainer");
  container.innerHTML = "";

  images.forEach((imgPath) => {
    const img = document.createElement("img");
    img.src = imgPath;
    img.style.width = "200px";
    img.style.margin = "10px";

    container.appendChild(img);
  });
}

async function processImages() {
  console.log("🎨 Generating images...");

  const jsonText = document.getElementById("jsonBox").value;

  let data;
  try {
    data = JSON.parse(jsonText);
  } catch {
    alert("Invalid JSON!");
    return;
  }

  const res = await fetch(`${API}/process-images`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(data)
  });

  const result = await res.json();

  console.log("🖼️ Images:", result);

  displayImages(result.images);
}

function displayImages(images) {
    const container = document.getElementById("image-container");
    container.innerHTML = "";

    images.forEach((img, index) => {
        const div = document.createElement("div");

        // extract relative path after /output/
        const relativePath = img.split("/output/")[1];

        div.innerHTML = `
            <img src="${img}" width="200"/>
            <br/>
            <a href="/download-image/${relativePath}">
                <button>⬇ Download</button>
            </a>
        `;

        container.appendChild(div);
    });
}


function generateAudio() {
    const jsonText = document.getElementById("jsonBox").value;

    console.log("📦 Raw JSON:", jsonText);

    if (!jsonText) {
        alert("JSON box is empty!");
        return;
    }

    // ✅ Parse JSON
    const data = JSON.parse(jsonText);

    const script = data.script_50_sec;

    console.log("🎙 Extracted script:", script);

    fetch("/generate-audio", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            script: script
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log("✅ Audio response:", data);
    });
}

function changeSpeed(speed) {
    const audio = document.getElementById("audioPlayer");
    audio.playbackRate = speed;
}



window.onload = () => {
  console.log("🚀 App loaded");
};