// Caching common elements with type annotations
const chatHistory = document.querySelector(".chat-history") as HTMLElement;

// Define an interface for our endpoints to ensure type safety
interface Endpoints {
  chatEndpoint: string;
}

const endpointBase: string = "http://127.0.0.1:8000";
const endpoints: Endpoints = {
  chatEndpoint: "/chat",
};

function initializeChatInput(): void {
  const chatInput = document.querySelector(".chat-input") as HTMLInputElement;

  if (chatInput && chatHistory) {
    chatInput.addEventListener("keypress", (e: KeyboardEvent) => {
      if (e.key === "Enter") {
        const chatInputValue = chatInput.value.trim();

        if (chatInputValue) {
          const userMessageDiv = document.createElement("div");
          userMessageDiv.classList.add("chat-history-chat");
          userMessageDiv.innerText = chatInputValue;
          chatHistory.appendChild(userMessageDiv);

          chatInput.value = "";

          sendMessage(chatInputValue);
        }
      }
    });
  }
}

/**
 * sends a message to the backend API.
 *
 * @param message The text message to send.
 * @param attachment An optional base64 string of an attachment.
 */
async function sendMessage(message: string, attachment: string | null = null): Promise<void> {
  try {
    const response = await fetch(endpointBase + endpoints.chatEndpoint, {
      method: "POST",
      mode: "cors",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message, attachment }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const res = await response.json();
    console.log(res);
  } catch (error) {
    console.error("Failed to send message:", error);
  }
}

/**
 * main setup function to initialize all event listeners.
 */
function setup(): void {
  initializeChatInput();
}

document.addEventListener("DOMContentLoaded", setup);