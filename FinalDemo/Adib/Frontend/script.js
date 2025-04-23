// === Navbar Active Link ===
document.addEventListener("DOMContentLoaded", () => {
    const path = window.location.pathname.split("/").pop() || "index.html"; // Default to index.html if path is empty
    const navLinks = document.querySelectorAll("nav a");

    navLinks.forEach(link => {
      const href = link.getAttribute("href");
      if (href === path) {
        link.classList.add("text-yellow-400");
      } else {
        link.classList.remove("text-yellow-400");
      }
    });

    // Initialize Lucide icons if they exist on the page
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // Add click listener to send button if it exists
    const sendButton = document.querySelector("button[data-lucide='send']");
     if (sendButton && chatInput && chatLog) {
        sendButton.addEventListener("click", handleSendMessage);
     }
});

// === Image Modal Functionality ===

document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modal-image');
    const closeModalBtn = document.getElementById('modal-close-btn');
    // Use a more specific class for clickable items if needed, otherwise query grids
    const insightImages = document.querySelectorAll('#insights-grid img, #model-results-grid img');
    const body = document.body;

    if (modal && modalImage && closeModalBtn && insightImages.length > 0) {
        console.log(`Found ${insightImages.length} insight images for modal.`);

        const openModal = (imgSrc, imgAlt) => {
            modalImage.src = imgSrc;
            modalImage.alt = imgAlt || "Enlarged Insight Visualization";

            // Remove hidden first (or ensure it's not display:none)
            // We rely on the CSS for initial state (opacity-0, invisible, scale-95)
            // The 'hidden' class might interfere, let's manage visibility via CSS classes instead
            modal.style.display = 'flex'; // Ensure it's display:flex

            // Force repaint/reflow before adding the visible class
            void modal.offsetWidth;

            // Add the class that triggers the transition
            modal.classList.add('modal-visible');
            body.style.overflow = 'hidden'; // Prevent background scrolling

            // Initialize close button icon if needed
            if (typeof lucide !== 'undefined') {
                const closeIcon = closeModalBtn.querySelector('i[data-lucide="x"]');
                if (closeIcon && !closeIcon.getAttribute('data-lucide-rendered')) {
                    lucide.createIcons({ nodes: [closeIcon] });
                    closeIcon.setAttribute('data-lucide-rendered', 'true');
                }
            }
        };

        const closeModal = () => {
            // Remove the class that makes it visible
            modal.classList.remove('modal-visible');
            body.style.overflow = ''; // Restore background scrolling

            // Wait for transition to finish before setting display: none
            // The CSS transition handles the visibility delay
             setTimeout(() => {
                  // Only hide if the visible class is still removed (safety check)
                  if (!modal.classList.contains('modal-visible')) {
                       modal.style.display = 'none';
                       modalImage.src = ""; // Clear src
                       modalImage.alt = "";
                  }
             }, 300); // Match the CSS transition duration
        };

        // Add listeners to each insight image
        insightImages.forEach(img => {
            // img.classList.add('cursor-pointer'); // Already added in HTML
            img.addEventListener('click', (e) => {
                e.stopPropagation();
                console.log(`Image clicked: ${img.src}`);
                openModal(img.src, img.alt);
            });
        });

        // Listener for the close button
        closeModalBtn.addEventListener('click', closeModal);

        // Listener to close modal when clicking the background overlay
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal();
            }
        });

        // Listener for the Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.classList.contains('modal-visible')) { // Check if modal is visible
                closeModal();
            }
        });

    } else if (document.getElementById('insights-grid')) {
         console.warn("Modal elements or insight images not found. Modal functionality disabled.");
    }

    // === NEW: Prediction Form Functionality ===
    const predictionForm = document.getElementById('prediction-form');
    const resultArea = document.getElementById('prediction-result-area');
    const resultValueElement = document.getElementById('predicted-demand-value');
    const resultStatusElement = document.getElementById('prediction-status');

    if (predictionForm && resultArea && resultValueElement && resultStatusElement) {
        predictionForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // Prevent default HTML form submission

            // Clear previous results and show loading state
            resultValueElement.textContent = '-- MW';
            resultStatusElement.textContent = 'Forecasting...';
            resultArea.classList.remove('hidden'); // Show the area
            resultArea.classList.remove('visible'); // Reset animation state if needed
            // Force reflow before adding class for animation
            void resultArea.offsetWidth;
            resultArea.classList.add('visible');

            // Get form data
            const formData = new FormData(predictionForm);
            const data = {};
            let formIsValid = true;

            // Convert FormData to JSON object and validate numbers
            for (const [key, value] of formData.entries()) {
                const numValue = (key === 'temp') ? parseFloat(value) : parseInt(value, 10);
                if (isNaN(numValue)) {
                    formIsValid = false;
                    resultStatusElement.textContent = `Error: Invalid input for ${key}. Please enter a number.`;
                    resultValueElement.textContent = 'Error';
                    console.error(`Invalid number format for ${key}: ${value}`);
                    break; // Stop processing if invalid
                }
                 // Basic range checks (optional but good)
                 if (key === 'month' && (numValue < 1 || numValue > 12)) formIsValid = false;
                 if (key === 'day' && (numValue < 1 || numValue > 31)) formIsValid = false;
                 if ((key === 'season' || key === 'isholiday') && (numValue !== 0 && numValue !== 1)) formIsValid = false;
                 if (!formIsValid) {
                    resultStatusElement.textContent = `Error: Invalid value for ${key}. Check range/format.`;
                    resultValueElement.textContent = 'Error';
                     console.error(`Invalid value for ${key}: ${value}`);
                    break;
                 }

                data[key] = numValue;
            }

            if (!formIsValid) {
                return; // Stop if validation failed
            }

            console.log("Sending data to backend:", data);

            try {
                const response = await fetch('http://localhost:8000/predict/', { // Adjust URL if needed
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                });

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({ detail: 'Unknown error structure' })); // Try to parse error
                    console.error("API Error Response:", errorData);
                    throw new Error(`API Error (${response.status}): ${errorData.detail || response.statusText}`);
                }

                const result = await response.json();

                if (result.predicted_demand !== undefined) {
                    // Format the result (e.g., to 2 decimal places)
                    const formattedDemand = parseFloat(result.predicted_demand).toFixed(2);
                    resultValueElement.textContent = `${formattedDemand} MW`;
                    resultStatusElement.textContent = 'Prediction successful.';
                    console.log("Prediction successful:", result.predicted_demand);
                } else {
                     throw new Error('Invalid response format from server.');
                }

            } catch (error) {
                console.error('Prediction failed:', error);
                resultValueElement.textContent = 'Error';
                resultStatusElement.textContent = `Prediction failed: ${error.message}`;
                // Make sure result area is visible to show the error
                resultArea.classList.remove('hidden');
                resultArea.classList.add('visible');
            }
        });
    }
    // === END: Prediction Form Functionality ===

    const infoModal = document.getElementById('infoModal');
    const accuracyInfoBtn = document.getElementById('accuracy-info-btn');
    const closeInfoBtn = document.getElementById('modal-close-btn-info'); // Use unique ID

    // Helper function to open the info modal
    const openInfoModal = () => {
        if (!infoModal) return; // Safety check
        console.log("Opening info modal...");
        infoModal.style.display = 'flex'; // Make it flex container
        // Force repaint/reflow before adding the visible class
        void infoModal.offsetWidth;
        infoModal.classList.add('modal-visible');
        document.body.style.overflow = 'hidden'; // Prevent background scrolling

        // Initialize close button icon if needed (should be handled by global init now)
        // Ensure Lucide is called if icons aren't rendering
        if (typeof lucide !== 'undefined') {
            const closeIcon = closeInfoBtn?.querySelector('i[data-lucide="x"]');
            if (closeIcon && !closeIcon.getAttribute('data-lucide-rendered')) {
                lucide.createIcons({ nodes: [closeIcon] });
                closeIcon.setAttribute('data-lucide-rendered', 'true'); // Mark as rendered
            }
        }
    };

    // Helper function to close the info modal
    const closeInfoModal = () => {
        if (!infoModal) return; // Safety check
        console.log("Closing info modal...");
        infoModal.classList.remove('modal-visible');
        document.body.style.overflow = ''; // Restore background scrolling

        // Wait for transition before setting display: none
        setTimeout(() => {
            // Only hide if the visible class is still removed
            if (!infoModal.classList.contains('modal-visible')) {
                infoModal.style.display = 'none';
            }
        }, 300); // Match the CSS transition duration
    };

    // Add event listeners if the elements exist
    if (infoModal && accuracyInfoBtn && closeInfoBtn) {
        // Listener for the trigger button in the result area
        accuracyInfoBtn.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent potential interference
            openInfoModal();
        });

        // Listener for the modal's close button
        closeInfoBtn.addEventListener('click', closeInfoModal);

        // Listener to close modal when clicking the background overlay
        infoModal.addEventListener('click', (e) => {
            // Check if the click is directly on the modal overlay (not the content inside)
            if (e.target === infoModal) {
                closeInfoModal();
            }
        });

        // Listener for the Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && infoModal.classList.contains('modal-visible')) {
                closeInfoModal();
            }
        });
    } else {
         // Log warning if elements aren't found on this page load
         if (!infoModal && document.getElementById('prediction-result-area')) console.warn("Info Modal container (#infoModal) not found.");
         if (!accuracyInfoBtn && document.getElementById('prediction-result-area')) console.warn("Accuracy Info Button (#accuracy-info-btn) not found.");
         if (!closeInfoBtn && document.getElementById('prediction-result-area')) console.warn("Info Modal Close Button (#modal-close-btn-info) not found.");
    }

    // Initialize other icons (navbar etc.)
     if (typeof lucide !== 'undefined') {
        console.log("Initializing Lucide icons globally...");
        lucide.createIcons();
     }

}); // End DOMContentLoaded

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
        const response = await fetch("http://localhost:8000/query/", {
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