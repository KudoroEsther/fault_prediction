const messagesContainer = document.getElementById("messagesContainer");
const form = document.getElementById("faultForm");
const analyzeBtn = document.getElementById("analyzeBtn");

const fields = ["Va", "Vb", "Vc", "Ia", "Ib", "Ic"];

function timestamp() {
    return new Date().toLocaleTimeString();
}

function addMessage(type, content, isHtml = false) {
    const wrapper = document.createElement("article");
    wrapper.className = `message ${type}`;
    wrapper.innerHTML = isHtml ? content : content.replace(/\n/g, "<br>");

    const time = document.createElement("small");
    time.textContent = timestamp();
    wrapper.appendChild(time);

    messagesContainer.appendChild(wrapper);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function readPayload() {
    const payload = {};
    for (const field of fields) {
        payload[field] = Number.parseFloat(document.getElementById(field).value);
    }
    return payload;
}

function resetForm() {
    form.reset();
}

function setLoading(isLoading) {
    analyzeBtn.disabled = isLoading;
    analyzeBtn.textContent = isLoading ? "Analyzing..." : "Analyze Fault";
}

addMessage(
    "bot",
    "Welcome to PowerBot. Enter the six transmission line readings to predict a fault and, when available, receive a RAG-based diagnosis."
);

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const payload = readPayload();

    if (Object.values(payload).some((value) => Number.isNaN(value))) {
        addMessage("bot", "<span class='error'>Please complete all six readings before submitting.</span>", true);
        return;
    }

    addMessage(
        "user",
        `Submitted readings\nVa: ${payload.Va}, Vb: ${payload.Vb}, Vc: ${payload.Vc}\nIa: ${payload.Ia}, Ib: ${payload.Ib}, Ic: ${payload.Ic}`
    );

    setLoading(true);

    try {
        const response = await fetch("http://localhost:8000/diagnose", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.detail || "Diagnosis request failed.");
        }

        const markdown = result.fault_label === "No fault"
            ? `## System Status: Normal\nNo fault detected.\n\nConfidence: **${(result.confidence * 100).toFixed(1)}%**`
            : `## Fault Detected\n**Type:** ${result.fault_label}\n\n${result.final_answer}`;

        addMessage("bot", marked.parse(markdown), true);
        resetForm();
    } catch (error) {
        addMessage("bot", `<span class='error'>${error.message}</span>`, true);
    } finally {
        setLoading(false);
    }
});
