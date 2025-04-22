// === Navbar Active Link ===
document.addEventListener("DOMContentLoaded", () => {
    const path = window.location.pathname.split("/").pop();
    const navLinks = document.querySelectorAll("nav a");
  
    navLinks.forEach(link => {
      const href = link.getAttribute("href");
      if (href === path) {
        link.classList.add("text-yellow-400");
      } else {
        link.classList.remove("text-yellow-400");
      }
    });
  });
  
  // === Home: Scroll to Ask Genius ===
  const scrollBtn = document.getElementById("explore-btn");
  if (scrollBtn) {
    scrollBtn.addEventListener("click", () => {
      window.location.href = "ask.html";
    });
  }
  
  // === Chat ===
  const chatInput = document.getElementById("chat-input");
  const chatLog = document.getElementById("chat-log");
  
  if (chatInput && chatLog) {
    chatInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && chatInput.value.trim() !== "") {
        const userMsg = chatInput.value.trim();
        appendMessage("You", userMsg, "user");
  
        showTypingIndicator();
  
        setTimeout(async () => {
          await streamLLMResponse(userMsg);
          removeTypingIndicator();
        }, 800);
  
        chatInput.value = "";
      }
    });
  }
  
  // === Append Message Bubble ===
  function appendMessage(sender, msg, type, timestamp = true) {
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  
    const bubble = document.createElement("div");
    bubble.className = `
      max-w-[75%] px-4 py-3 rounded-xl text-sm 
      ${type === "user" ? "bg-white/10 self-end text-white" : "bg-yellow-400/10 self-start text-white"}
      animate-fade-in shadow-sm`;
  
    bubble.innerHTML = `
      <div class="text-xs mb-1 ${type === "user" ? "text-gray-400 text-right" : "text-yellow-400"} font-semibold">
        ${sender}
      </div>
      <div>${msg}</div>
      ${timestamp ? `<div class="text-[10px] text-gray-500 mt-1 ${type === "user" ? "text-right" : "text-left"}">${time}</div>` : ""}
    `;
  
    const wrapper = document.createElement("div");
    wrapper.className = `flex flex-col ${type === "user" ? "items-end" : "items-start"}`;
    wrapper.appendChild(bubble);
  
    chatLog.appendChild(wrapper);
    chatLog.scrollTop = chatLog.scrollHeight;
  }
  
  // === Typing Indicator ===
  function showTypingIndicator() {
    const typingDiv = document.createElement("div");
    typingDiv.id = "typing-indicator";
    typingDiv.className = "text-yellow-400 text-sm italic mb-2 animate-pulse";
    typingDiv.innerText = "GridGenius is thinking...";
    chatLog.appendChild(typingDiv);
    chatLog.scrollTop = chatLog.scrollHeight;
  }
  
  function removeTypingIndicator() {
    const typingDiv = document.getElementById("typing-indicator");
    if (typingDiv) typingDiv.remove();
  }
  
  // === Streaming LLM Response ===
  let chatHistory = [];

  async function streamLLMResponse(userInput) {
    try {
      chatHistory.push({ role: "user", content: userInput });
  
      // Limit chatHistory to last 10 exchanges (5 user + 5 assistant)
      if (chatHistory.length > 10) {
        chatHistory = chatHistory.slice(chatHistory.length - 10);
      }
  
      const response = await fetch("http://localhost:8000/query/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chat_history: chatHistory })
      });
  
      const data = await response.json();
      const botMessage = data.answer || "⚡ No answer received.";
  
      chatHistory.push({ role: "assistant", content: botMessage });
  
      // Again keep max 10 messages after bot reply
      if (chatHistory.length > 10) {
        chatHistory = chatHistory.slice(chatHistory.length - 10);
      }
  
      appendMessage("GridGenius", botMessage, "bot");
  
    } catch (err) {
      console.error("Error fetching from RAG backend:", err);
      appendMessage("GridGenius", "⚠️ GridGenius is offline or unavailable.", "bot");
    }
  }
  