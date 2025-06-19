js


const chat = document.getElementById("chat");
const userInput = document.getElementById("userInput");
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
const synth = window.speechSynthesis;

recognition.lang = "en-US";
recognition.interimResults = false;
recognition.maxAlternatives = 1;

function startRecognition() {
  recognition.start();

  recognition.onresult = async (event) => {
    const userText = event.results[0][0].transcript;
    addBubble(userText, "user");
    await getBotResponse(userText);
  };

 recognition.onerror = (event) => {
  if (event.error === "no-speech") {
    alert("🎤 Didn't catch that. Try speaking louder or closer to the mic.");
  } else {
    alert("Voice recognition error: " + event.error);
  }
};
}

function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;
  addBubble(message, "user");
  userInput.value = "";
  getBotResponse(message);
}

async function getBotResponse(message) {
  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const data = await res.json();
    const botReply = data.reply || data.response || "🤖 No response.";
    addBubble(botReply, "bot");
    speak(botReply);
  } catch (error) {
    addBubble("⚠️ Error: Couldn't reach the server.", "bot");
  }
}

function addBubble(text, sender) {
  const bubble = document.createElement("div");
  bubble.classList.add("bubble", sender);
  bubble.textContent = text;
  chat.appendChild(bubble);
  chat.scrollTop = chat.scrollHeight;
}

function speak(text) {
  const utter = new SpeechSynthesisUtterance(text);
  synth.speak(utter);
}

// Send message on Enter key
userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    sendMessage();
  }
});
