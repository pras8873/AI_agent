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
