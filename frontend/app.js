const API = "http://localhost:5000";

async function generate() {
  const topic = document.getElementById("topic").value;

  const res = await fetch(`${API}/generate`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ topic })
  });

  const data = await res.json();
  document.getElementById("jsonBox").value =
    JSON.stringify(data, null, 2);
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
