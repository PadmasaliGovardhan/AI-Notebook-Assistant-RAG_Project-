const backendURL = "http://127.0.0.1:8000"; // change if deployed
const uploadBtn = document.getElementById("uploadBtn");
const sendBtn = document.getElementById("sendBtn");
const pdfInput = document.getElementById("pdfInput");
const uploadStatus = document.getElementById("uploadStatus");
const chatBox = document.getElementById("chatBox");
const userInput = document.getElementById("userInput");

// ---------- Upload ----------
uploadBtn.addEventListener("click", async () => {
    const file = pdfInput.files[0];
    if (!file) return showStatus("⚠️ Please select a PDF first!", "orange");

    const formData = new FormData();
    formData.append("file", file);

    showStatus("📤 Uploading…", "#ffba08");
    try {
        const res = await fetch(`${backendURL}/upload_pdf/`, {
            method: "POST",
            body: formData,
        });
        const data = await res.json();
        showStatus(data.message || "✅ Upload complete!", "#4ade80");
    } catch (e) {
        showStatus("❌ Upload failed.", "#ef4444");
    }
});

function showStatus(txt, color) {
    uploadStatus.textContent = txt;
    uploadStatus.style.color = color;
}

// ---------- Chat ----------
sendBtn.addEventListener("click", sendQuery);
userInput.addEventListener("keydown", e => { if (e.key === "Enter") sendQuery(); });

async function sendQuery() {
    const query = userInput.value.trim();
    if (!query) return;
    appendMessage(query, "user");
    userInput.value = "";
    const thinking = appendMessage("Thinking…", "bot");

    const formData = new URLSearchParams();
    formData.append("query", query);

    try {
        const res = await fetch(`${backendURL}/ask/`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: formData,
        });
        const data = await res.json();
        chatBox.removeChild(thinking);
        appendMessage(data.answer || "⚠️ No response from model.", "bot", true);
    } catch (err) {
        console.error(err);
        chatBox.removeChild(thinking);
        appendMessage("❌ Error connecting to backend.", "bot");
    }
}

// ---------- Message Helper ----------
function appendMessage(text, sender, isMarkdown = false) {
    const div = document.createElement("div");
    div.className = `message ${sender}`;
    if (isMarkdown) {
        div.innerHTML = marked.parse(text);
    } else {
        div.textContent = text;
    }
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
    return div;
}
