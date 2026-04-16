const API = "http://localhost:5000";

async function generate() {
  console.log("🔥 Generate button clicked");

  const topic = document.getElementById("topic").value;
  console.log("📌 Topic:", topic);

  try {
    const res = await fetch(`/generate`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
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

async function process() {
  const jsonData = JSON.parse(
    document.getElementById("jsonBox").value
  );

  await fetch(`${API}/process`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(jsonData)
  });

  alert("Done!");
}

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

  // 🔥 Get AI Pipe token from URL
  const params = new URLSearchParams(window.location.search);
  const token = params.get("aipipe_token");

  if (!token) {
    alert("Please login via AI Pipe first");
    return;
  }

  data.token = token;

  const res = await fetch("/process-images", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(data)
  });

  const result = await res.json();

  console.log(result);

  displayImages(result.images);
}
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

function ensureLogin() {
  const params = new URLSearchParams(window.location.search);

  let tokenFromUrl = params.get("aipipe_token");

  // ✅ If token comes from AI Pipe redirect → save it
  if (tokenFromUrl) {
    console.log("✅ Token received from URL");

    localStorage.setItem("aipipe_token", tokenFromUrl);

    // 🔥 Clean URL (remove token from address bar)
    window.history.replaceState({}, document.title, window.location.pathname);

    return tokenFromUrl;
  }

  // ✅ Otherwise use stored token
  const storedToken = localStorage.getItem("aipipe_token");

  if (storedToken) {
    console.log("✅ Using stored token");
    return storedToken;
  }

  // ❌ If no token → redirect to login
  console.log("❌ No token → redirecting to login");

  window.location.href =
    "https://aipipe.org/login?redirect=" +
    encodeURIComponent(window.location.href);

  return null;
}
window.onload = () => {
  ensureLogin();
};