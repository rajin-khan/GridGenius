document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded and parsed"); // Add this for debugging

    // === 1. Define Core Variables (if needed globally within listener) ===
    const body = document.body;

    // === 2. Navbar Active Link ===
    const path = window.location.pathname.split("/").pop() || "index.html";
    const navLinks = document.querySelectorAll("nav a");
    console.log(`Current path: ${path}`);
    navLinks.forEach(link => {
        const href = link.getAttribute("href");
        if (href === path) {
            link.classList.add("text-yellow-400");
            console.log(`Activating link: ${href}`);
        } else {
            link.classList.remove("text-yellow-400");
        }
    });

    // === 3. Image Modal Functionality (Conditional) ===
    const imageModal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modal-image');
    const imageModalCloseBtn = document.getElementById('modal-close-btn'); // Renamed to avoid conflict
    const insightImages = document.querySelectorAll('#insights-grid img, #model-results-grid img');

    // Only run modal logic if the necessary elements exist (likely on insights.html)
    if (imageModal && modalImage && imageModalCloseBtn && insightImages.length > 0) {
        console.log(`Image Modal Setup: Found ${insightImages.length} insight images.`);

        const openImageModal = (imgSrc, imgAlt) => { // Renamed to be specific
            modalImage.src = imgSrc;
            modalImage.alt = imgAlt || "Enlarged Insight Visualization";
            imageModal.style.display = 'flex';
            void imageModal.offsetWidth; // Reflow
            imageModal.classList.add('modal-visible');
            body.style.overflow = 'hidden';
        };

        const closeImageModal = () => { // Renamed to be specific
            imageModal.classList.remove('modal-visible');
            body.style.overflow = '';
            setTimeout(() => {
                if (!imageModal.classList.contains('modal-visible')) {
                    imageModal.style.display = 'none';
                    modalImage.src = "";
                    modalImage.alt = "";
                }
            }, 300);
        };

        insightImages.forEach(img => {
            img.addEventListener('click', (e) => {
                e.stopPropagation();
                console.log(`Image clicked: ${img.src}`);
                openImageModal(img.src, img.alt);
            });
        });

        imageModalCloseBtn.addEventListener('click', closeImageModal);

        imageModal.addEventListener('click', (e) => {
            if (e.target === imageModal) {
                closeImageModal();
            }
        });
        // We'll add the Escape key listener globally later
    } else if (document.getElementById('insights-grid')) {
        console.warn("Image Modal elements or insight images not found, but insights grid exists.");
    }

    // === 4. Prediction Form Functionality (Conditional) ===
    const predictionForm = document.getElementById('prediction-form');
    const resultArea = document.getElementById('prediction-result-area');
    const resultValueElement = document.getElementById('predicted-demand-value');
    const resultStatusElement = document.getElementById('prediction-status');

    // Only run prediction logic if the form exists (likely on predict.html)
    if (predictionForm && resultArea && resultValueElement && resultStatusElement) {
        console.log("Prediction Form Setup: Elements found.");
        predictionForm.addEventListener('submit', async (event) => {
             event.preventDefault();
             console.log("Prediction form submitted.");
             // Show loading state
             resultValueElement.textContent = '-- MW';
             resultStatusElement.textContent = 'Forecasting...';
             resultArea.classList.remove('hidden');
             resultArea.classList.remove('visible');
             void resultArea.offsetWidth; // Reflow
             resultArea.classList.add('visible');

             const formData = new FormData(predictionForm);
             const data = {};
             let formIsValid = true;

             // Basic validation and data preparation
             for (const [key, value] of formData.entries()) {
                const numValue = (key === 'temp') ? parseFloat(value) : parseInt(value, 10);
                 if (isNaN(numValue) ||
                    (key === 'month' && (numValue < 1 || numValue > 12)) ||
                    (key === 'day' && (numValue < 1 || numValue > 31)) ||
                    ((key === 'season' || key === 'isholiday') && (numValue !== 0 && numValue !== 1)) )
                 {
                     formIsValid = false;
                     resultStatusElement.textContent = `Error: Invalid value for ${key}. Check range/format.`;
                     resultValueElement.textContent = 'Error';
                     console.error(`Invalid value/format for ${key}: ${value}`);
                     break;
                 }
                 data[key] = numValue;
             }

             if (!formIsValid) return;

             console.log("Sending prediction data:", data);
             try {
                 const response = await fetch('https://gridgenius-production.up.railway.app/predict/', {
                     method: 'POST',
                     headers: { 'Content-Type': 'application/json' },
                     body: JSON.stringify(data),
                 });
                 if (!response.ok) {
                     const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
                     throw new Error(`API Error (${response.status}): ${errorData.detail || response.statusText}`);
                 }
                 const result = await response.json();
                 if (result.predicted_demand !== undefined) {
                     const formattedDemand = parseFloat(result.predicted_demand).toFixed(2);
                     resultValueElement.textContent = `${formattedDemand} MW`;
                     resultStatusElement.textContent = 'Prediction successful.';
                     console.log("Prediction result:", result.predicted_demand);
                 } else {
                     throw new Error('Invalid response format.');
                 }
             } catch (error) {
                 console.error('Prediction failed:', error);
                 resultValueElement.textContent = 'Error';
                 resultStatusElement.textContent = `Prediction failed: ${error.message}`;
                 resultArea.classList.remove('hidden'); // Ensure error is visible
                 resultArea.classList.add('visible');
             }
        });
    }

    // === 5. Info Modal (Accuracy) Functionality (Conditional) ===
    const infoModal = document.getElementById('infoModal');
    const accuracyInfoBtn = document.getElementById('accuracy-info-btn');
    const closeInfoBtn = document.getElementById('modal-close-btn-info');

    // Only run info modal logic if elements exist (likely on predict.html)
    if (infoModal && accuracyInfoBtn && closeInfoBtn) {
        console.log("Info Modal Setup: Elements found.");
        const openInfoModal = () => {
            infoModal.style.display = 'flex';
            void infoModal.offsetWidth; // Reflow
            infoModal.classList.add('modal-visible');
            body.style.overflow = 'hidden';
        };
        const closeInfoModal = () => {
            infoModal.classList.remove('modal-visible');
            body.style.overflow = '';
            setTimeout(() => {
                if (!infoModal.classList.contains('modal-visible')) {
                    infoModal.style.display = 'none';
                }
            }, 300);
        };

        accuracyInfoBtn.addEventListener('click', (e) => { e.stopPropagation(); openInfoModal(); });
        closeInfoBtn.addEventListener('click', closeInfoModal);
        infoModal.addEventListener('click', (e) => { if (e.target === infoModal) closeInfoModal(); });
        // We'll add the Escape key listener globally later
    }

    // === 6. Feature Modal (Homepage) Functionality (Conditional) ===
    const featureCards = document.querySelectorAll('.feature-card');
    const featureModals = document.querySelectorAll('.feature-modal');
    const featureModalCloseBtns = document.querySelectorAll('.modal-close-feature');

     // Only run feature modal logic if cards exist (likely on index.html)
    if (featureCards.length > 0 && featureModals.length > 0) {
        console.log(`Feature Modal Setup: Found ${featureCards.length} cards.`);
        const closeAllFeatureModals = () => {
            featureModals.forEach(modal => {
                modal.classList.remove('modal-visible');
            });
             // Only restore scroll if no *other* modals are open
             if (!document.querySelector('#infoModal.modal-visible, #imageModal.modal-visible')) {
                  body.style.overflow = '';
             }
             // No need for timeout/display:none if using visibility+opacity
        };

        const openFeatureModal = (modalId) => {
            // Close other *feature* modals first
            featureModals.forEach(m => m.classList.remove('modal-visible'));

            const targetModal = document.querySelector(modalId);
            if (targetModal) {
                // targetModal.style.display = 'flex'; // Let CSS handle display via visibility
                void targetModal.offsetWidth; // Reflow
                targetModal.classList.add('modal-visible');
                body.style.overflow = 'hidden';
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons({ nodes: targetModal.querySelectorAll('[data-lucide]') });
                }
            } else {
                console.error(`Feature Modal with ID ${modalId} not found.`);
            }
        };

        featureCards.forEach(card => {
            card.addEventListener('click', () => {
                const modalId = card.getAttribute('data-modal-target');
                console.log(`Feature card clicked, target: ${modalId}`);
                if (modalId) { openFeatureModal(modalId); }
            });
        });

        featureModalCloseBtns.forEach(btn => {
             btn.addEventListener('click', (e) => { e.stopPropagation(); closeAllFeatureModals(); });
        });

        featureModals.forEach(modal => {
             modal.addEventListener('click', (e) => { if (e.target === modal) closeAllFeatureModals(); });
        });
        // We'll add the Escape key listener globally later
    }

    // === 7. Chat Functionality (Conditional) ===
    const chatInput = document.getElementById("chat-input");
    const chatLog = document.getElementById("chat-log");
    const chatSendButton = document.querySelector("button[aria-label='Send message']"); // CORRECT SELECTOR
    let chatHistory = []; // Keep chat history scoped if only needed here

    // Only run chat logic if elements exist (likely on ask.html)
    if (chatInput && chatLog && chatSendButton) {
        console.log("Chat Setup: Elements found.");

        // --- Define Chat Helper Functions INSIDE the conditional block ---
        const appendMessage = (sender, msg, type, timestamp = true) => {
             // (Keep your existing appendMessage function code here)
             const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
             const bubble = document.createElement("div");
             bubble.className = `max-w-[75%] px-4 py-3 rounded-xl text-sm ${type === "user" ? "bg-white/10 self-end text-white" : "bg-yellow-400/10 self-start text-white"} animate-fade-in shadow-sm message-bubble`;
             const contentHTML = (type === "bot") ? marked.parse(msg) : escapeHTML(msg);
             bubble.innerHTML = `<div class="text-xs mb-1 ${type === "user" ? "text-gray-400 text-right" : "text-yellow-400"} font-semibold">${sender}</div><div class="message-content prose prose-invert prose-sm max-w-none">${contentHTML}</div>${timestamp ? `<div class="timestamp text-[10px] text-gray-500 mt-1 ${type === "user" ? "text-right" : "text-left"}">${time}</div>` : ""}`;
             const wrapper = document.createElement("div");
             wrapper.className = `flex flex-col ${type === "user" ? "items-end" : "items-start"}`;
             wrapper.appendChild(bubble);
             chatLog.appendChild(wrapper);
             // Auto-scroll
             setTimeout(() => { // Slight delay allows content to render before scroll calc
                chatLog.scrollTop = chatLog.scrollHeight;
             }, 50);
             return bubble;
        };

        const escapeHTML = (str) => {
             const div = document.createElement('div');
             div.textContent = str;
             return div.innerHTML;
        };

        const showTypingIndicator = () => {
             removeTypingIndicator();
             const typingDiv = document.createElement("div");
             typingDiv.id = "typing-indicator";
             typingDiv.className = `flex flex-col items-start`;
             typingDiv.innerHTML = `<div class="max-w-[75%] px-4 py-3 rounded-xl text-sm bg-yellow-400/10 self-start text-white animate-pulse shadow-sm"><div class="text-xs mb-1 text-yellow-400 font-semibold">GridGenius</div><div>Thinking...</div></div>`;
             chatLog.appendChild(typingDiv);
             chatLog.scrollTop = chatLog.scrollHeight;
        };

        const removeTypingIndicator = () => {
             const typingDiv = document.getElementById("typing-indicator");
             if (typingDiv) typingDiv.remove();
        };

        const streamLLMResponse = async (currentChatHistory) => {
             // (Keep your existing streamLLMResponse function code here, using the appendMessage defined above)
             // Make sure it uses the correct backend URL
             let botMessageBubble = null;
             let botContentElement = null;
             let accumulatedResponse = "";
             const decoder = new TextDecoder();
             try {
                 const response = await fetch("https://gridgenius-production.up.railway.app/query/", { // Make sure URL is correct
                     method: "POST",
                     headers: { "Content-Type": "application/json" },
                     body: JSON.stringify({ chat_history: currentChatHistory })
                 });
                 removeTypingIndicator();
                 if (!response.ok) {
                     const errorText = await response.text();
                     throw new Error(`API Error (${response.status}): ${errorText}`);
                 }
                 const reader = response.body.getReader();
                 botMessageBubble = appendMessage("GridGenius", "", "bot", false);
                 botContentElement = botMessageBubble.querySelector(".message-content");
                 if (!botContentElement) throw new Error("Could not find .message-content in bot bubble");
                 botContentElement.innerHTML = ''; // Start empty

                 while (true) {
                     const { value, done } = await reader.read();
                     if (done) {
                         const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                         const timestampDiv = document.createElement('div');
                         timestampDiv.className = "timestamp text-[10px] text-gray-500 mt-1 text-left";
                         timestampDiv.textContent = time;
                         botMessageBubble.appendChild(timestampDiv);
                         chatHistory.push({ role: "assistant", content: accumulatedResponse }); // Update shared history
                         if (chatHistory.length > 10) { // Limit history
                             chatHistory = chatHistory.slice(-10);
                         }
                         break;
                     }
                     const chunk = decoder.decode(value, { stream: true });
                     accumulatedResponse += chunk;
                     botContentElement.innerHTML = marked.parse(accumulatedResponse);
                     chatLog.scrollTop = chatLog.scrollHeight;
                 }
             } catch (err) {
                 console.error("Error fetching/streaming:", err);
                 removeTypingIndicator();
                 if (botContentElement) { botContentElement.innerHTML += "<br>⚠️ Error receiving full response."; }
                 else { appendMessage("GridGenius", `⚠️ Streaming Error: ${err.message}`, "bot"); }
             }
        };

        const handleSendMessage = () => { // Define handler INSIDE conditional block
             const userMsg = chatInput.value.trim();
             if (userMsg !== "") {
                 appendMessage("You", userMsg, "user");
                 chatHistory.push({ role: "user", content: userMsg });
                 if (chatHistory.length > 10) { // Limit history
                     chatHistory = chatHistory.slice(-10);
                 }
                 showTypingIndicator();
                 streamLLMResponse(chatHistory).catch(err => { // Pass current history
                     console.error("Streaming error triggered:", err);
                     removeTypingIndicator();
                     appendMessage("GridGenius", "⚠️ Error receiving response.", "bot");
                 });
                 chatInput.value = "";
             }
        };
        // --- End Chat Helper Functions ---

        // Attach listeners using the locally defined handler
        chatInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSendMessage(); // Call the handler
            }
        });

        chatSendButton.addEventListener("click", handleSendMessage); // Call the handler

        console.log("Chat listeners attached.");

    } else if (document.getElementById('chat-log-container')) {
         console.warn("Chat input or button not found, but chat container exists.");
    }

    // === 8. Global Escape Key Listener for ALL Modals ===
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            console.log("Escape key pressed");
             // Check and close relevant modals
            if (imageModal && imageModal.classList.contains('modal-visible')) {
                 console.log("Closing image modal via Escape");
                 closeImageModal(); // Use specific close function if defined
            } else if (infoModal && infoModal.classList.contains('modal-visible')) {
                console.log("Closing info modal via Escape");
                closeInfoModal(); // Use specific close function if defined
            } else {
                 // Check feature modals (need access to closeAllFeatureModals or re-select)
                  const anyFeatureModalVisible = Array.from(featureModals).some(m => m.classList.contains('modal-visible'));
                  if (anyFeatureModalVisible) {
                       console.log("Closing feature modal via Escape");
                       closeAllFeatureModals(); // Use the function defined in section 6
                  }
            }
        }
    });

    // === 9. Global Lucide Initialization ===
    // Call this once at the very end after all potential elements are checked/listeners attached
    if (typeof lucide !== 'undefined') {
        console.log("Initializing Lucide icons globally...");
        lucide.createIcons();
        // Mark icons as rendered after global init (optional, good practice)
        document.querySelectorAll('[data-lucide]').forEach(iconEl => iconEl.setAttribute('data-lucide-rendered', 'true'));
    } else {
         console.error("Lucide library not loaded!");
    }

}); // === END DOMContentLoaded ===

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
let chatHistory = []; // Keep track of the conversation

// Function to handle sending message (used by Enter key and button click)
function handleSendMessage() {
    if (chatInput.value.trim() !== "") {
        const userMsg = chatInput.value.trim();
        appendMessage("You", userMsg, "user");
        chatHistory.push({ role: "user", content: userMsg });

        // Limit chatHistory before sending
        if (chatHistory.length > 10) {
          chatHistory = chatHistory.slice(chatHistory.length - 10);
        }

        showTypingIndicator();

        // Call the streaming function
        streamLLMResponse(chatHistory)
          .catch(err => {
              console.error("Error during streaming:", err);
              removeTypingIndicator();
              appendMessage("GridGenius", "⚠️ Error receiving response.", "bot");
          });

        chatInput.value = "";
    }
}

if (chatInput && chatLog) {
  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) { // Allow Shift+Enter for newlines if needed later
      e.preventDefault(); // Prevent default newline insertion
      handleSendMessage();
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
    animate-fade-in shadow-sm message-bubble`; // Add message-bubble class

  // Use marked.parse for bot messages to render markdown
  const contentHTML = (type === "bot") ? marked.parse(msg) : escapeHTML(msg); // Escape user HTML

  bubble.innerHTML = `
    <div class="text-xs mb-1 ${type === "user" ? "text-gray-400 text-right" : "text-yellow-400"} font-semibold">
      ${sender}
    </div>
    <div class="message-content prose prose-invert prose-sm max-w-none">${contentHTML}</div>
    ${timestamp ? `<div class="timestamp text-[10px] text-gray-500 mt-1 ${type === "user" ? "text-right" : "text-left"}">${time}</div>` : ""}
  `;

  const wrapper = document.createElement("div");
  wrapper.className = `flex flex-col ${type === "user" ? "items-end" : "items-start"}`;
  wrapper.appendChild(bubble);

  chatLog.appendChild(wrapper);
  chatLog.scrollTop = chatLog.scrollHeight; // Scroll to bottom

  return bubble; // Return the created bubble element
}

// Helper to escape HTML
function escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}


// === Typing Indicator ===
function showTypingIndicator() {
  // Remove existing indicator first if any
  removeTypingIndicator();
  const typingDiv = document.createElement("div");
  typingDiv.id = "typing-indicator";
  // Use bot styling for consistency
  typingDiv.className = `flex flex-col items-start`;
  typingDiv.innerHTML = `
      <div class="max-w-[75%] px-4 py-3 rounded-xl text-sm bg-yellow-400/10 self-start text-white animate-pulse shadow-sm">
          <div class="text-xs mb-1 text-yellow-400 font-semibold">GridGenius</div>
          <div>Thinking...</div>
      </div>
  `;
  chatLog.appendChild(typingDiv);
  chatLog.scrollTop = chatLog.scrollHeight;
}

function removeTypingIndicator() {
  const typingDiv = document.getElementById("typing-indicator");
  if (typingDiv) typingDiv.remove();
}


// === Streaming LLM Response ===
async function streamLLMResponse(currentChatHistory) {
    let botMessageBubble = null;
    let botContentElement = null;
    let accumulatedResponse = "";
    const decoder = new TextDecoder();

    try {
        const response = await fetch("https://gridgenius-production.up.railway.app/query/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ chat_history: currentChatHistory }) // Send current history
        });

        removeTypingIndicator(); // Remove indicator once stream starts

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`API Error (${response.status}): ${errorText}`);
        }

        const reader = response.body.getReader();

        // Create the initial bubble (empty or with a placeholder)
        // Create bubble without timestamp initially
        botMessageBubble = appendMessage("GridGenius", "", "bot", false);
        botContentElement = botMessageBubble.querySelector(".message-content");
        if (!botContentElement) {
            console.error("Could not find .message-content in bot bubble");
            return; // Exit if structure is wrong
        }
        botContentElement.innerHTML = ''; // Start empty

        while (true) {
            const { value, done } = await reader.read();
            if (done) {
                // Add timestamp once message is complete
                const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                const timestampDiv = document.createElement('div');
                timestampDiv.className = "timestamp text-[10px] text-gray-500 mt-1 text-left";
                timestampDiv.textContent = time;
                botMessageBubble.appendChild(timestampDiv); // Append timestamp at the end

                // Add final response to client-side history AFTER stream is done
                chatHistory.push({ role: "assistant", content: accumulatedResponse });
                // Limit history again after bot reply
                 if (chatHistory.length > 10) {
                    chatHistory = chatHistory.slice(chatHistory.length - 10);
                 }
                break; // Exit the loop
            }

            const chunk = decoder.decode(value, { stream: true });
            accumulatedResponse += chunk;

            // Render markdown progressively
            botContentElement.innerHTML = marked.parse(accumulatedResponse);

            chatLog.scrollTop = chatLog.scrollHeight; // Keep scrolling to bottom
        }

    } catch (err) {
        console.error("Error fetching or streaming from RAG backend:", err);
        removeTypingIndicator(); // Ensure indicator is removed on error
        // If a bubble was partially created, indicate error there or add a new one
        if (botContentElement) {
             botContentElement.innerHTML += "<br>⚠️ Error receiving full response.";
        } else {
             appendMessage("GridGenius", `⚠️ Streaming Error: ${err.message}`, "bot");
        }
        // Don't add potentially broken response to history
    }
}