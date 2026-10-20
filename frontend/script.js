// ==========================================================================
// AI Assistant Chatbot - Frontend Script
// ==========================================================================

document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements
    const chatMessages = document.getElementById("chatMessages");
    const chatForm = document.getElementById("chatForm");
    const messageInput = document.getElementById("messageInput");
    const sendBtn = document.getElementById("sendBtn");

    // Backend API Configuration
    const API_URL = "http://localhost:8000/api/chat";

    /**
     * Scroll the chat window to the bottom smoothly
     */
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    /**
     * Dynamically create and append a message element to the chat window
     * @param {'user' | 'bot' | 'error'} type - Message origin/style
     * @param {string} text - Message content
     */
    function appendMessage(type, text) {
        const row = document.createElement("div");
        row.classList.add("message-row");

        if (type === "user") {
            row.classList.add("user-row");

            const bubble = document.createElement("div");
            bubble.classList.add("message-bubble");
            bubble.textContent = text;
            row.appendChild(bubble);
        } else if (type === "bot") {
            row.classList.add("bot-row");

            const avatar = document.createElement("div");
            avatar.classList.add("bot-avatar-small");
            avatar.setAttribute("aria-hidden", "true");
            avatar.textContent = "🤖";

            const bubble = document.createElement("div");
            bubble.classList.add("message-bubble");
            bubble.textContent = text;

            row.appendChild(avatar);
            row.appendChild(bubble);
        } else if (type === "error") {
            row.classList.add("error-row");

            const bubble = document.createElement("div");
            bubble.classList.add("message-bubble");
            bubble.textContent = text;
            row.appendChild(bubble);
        }

        chatMessages.appendChild(row);
        scrollToBottom();
    }

    /**
     * Display the 'Typing...' animated indicator while awaiting backend response
     */
    function showTypingIndicator() {
        if (document.getElementById("typingIndicator")) return;

        const row = document.createElement("div");
        row.id = "typingIndicator";
        row.classList.add("message-row", "bot-row");

        const avatar = document.createElement("div");
        avatar.classList.add("bot-avatar-small");
        avatar.setAttribute("aria-hidden", "true");
        avatar.textContent = "🤖";

        const bubble = document.createElement("div");
        bubble.classList.add("message-bubble", "typing-bubble");

        const dot1 = document.createElement("span");
        dot1.classList.add("typing-dot");
        const dot2 = document.createElement("span");
        dot2.classList.add("typing-dot");
        const dot3 = document.createElement("span");
        dot3.classList.add("typing-dot");

        const textSpan = document.createElement("span");
        textSpan.classList.add("typing-text");
        textSpan.textContent = "Typing...";

        bubble.appendChild(dot1);
        bubble.appendChild(dot2);
        bubble.appendChild(dot3);
        bubble.appendChild(textSpan);

        row.appendChild(avatar);
        row.appendChild(bubble);

        chatMessages.appendChild(row);
        scrollToBottom();
    }

    /**
     * Remove the typing indicator from the chat window
     */
    function removeTypingIndicator() {
        const indicator = document.getElementById("typingIndicator");
        if (indicator) {
            indicator.remove();
        }
    }

    /**
     * Toggle input and send button disabled states
     * @param {boolean} disabled
     */
    function setFormDisabled(disabled) {
        messageInput.disabled = disabled;
        sendBtn.disabled = disabled;
    }

    /**
     * Send user message to the backend and handle the response
     */
    async function sendMessage() {
        const rawMessage = messageInput.value;
        const trimmedMessage = rawMessage.trim();

        // Disallow empty messages
        if (!trimmedMessage) {
            return;
        }

        // 1. Immediately append user's message
        appendMessage("user", trimmedMessage);

        // 2. Clear input field immediately
        messageInput.value = "";

        // 3. Display typing state and disable input
        showTypingIndicator();
        setFormDisabled(true);

        try {
            // 4. Send POST request to backend
            const response = await fetch(API_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    message: trimmedMessage,
                }),
            });

            if (!response.ok) {
                let errorMessage = `Server error (${response.status})`;
                try {
                    const errorData = await response.json();
                    if (errorData && errorData.detail) {
                        errorMessage = typeof errorData.detail === "string" 
                            ? errorData.detail 
                            : JSON.stringify(errorData.detail);
                    }
                } catch {
                    // response is not JSON
                }
                throw new Error(errorMessage);
            }

            const data = await response.json();

            // 5. Remove typing indicator & display bot response
            removeTypingIndicator();
            appendMessage("bot", data.response || "No response received.");
        } catch (error) {
            // 6. Graceful error handling
            removeTypingIndicator();
            console.error("Chatbot communication error:", error);
            appendMessage(
                "error",
                "⚠️ Unable to reach the assistant server. Please verify the backend is running at " + API_URL
            );
        } finally {
            // 7. Re-enable form controls and refocus input
            setFormDisabled(false);
            messageInput.focus();
            scrollToBottom();
        }
    }

    // Event Listeners
    chatForm.addEventListener("submit", (e) => {
        e.preventDefault();
        sendMessage();
    });

    // Enter key sends message (without Shift key)
    messageInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Initial greeting dynamically added on startup
    appendMessage("bot", "Hello! How can I help you?");
    messageInput.focus();
});
