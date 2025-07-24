//caching common calls
const chatHistory = document.querySelector(".chat-history");
const endpointBase = "http://127.0.0.1:8000"
const endpoints = {
    "chatEndpoint" : "/chat"
}

function chatInputListener() {
    /**
     * sets up the event listener for the chat input
     */
    const chatInput = document.querySelector(".chat-input");
    chatInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            const chatInputValue = chatInput.value;
            chatInput.value = "";
            // add the text node to chatHistory
            const textNode = document.createElement('div')
            textNode.classList.add("chat-history-chat")
            textNode.innerText = chatInputValue;
            chatHistory.appendChild(textNode);
            // send a chat using sendMessage
            sendMessage(chatInputValue);
        }
    });
}

function setEventListeners() {
    /**
     * Creates the EventListeners to the the required elements
     */
    chatInputListener()
}

function setUp() {
    /**
     * setup function to be called on window load
     */
    setEventListeners()
}

async function sendMessage(message, attachment) {
    /**
     * sends a message to the backend with message
     *  Params:
     *      message (str): the mesasge
     *      attachment (str): the attachment as b64 str
     *  Returns:
     *      resp: the response object
     */ 
    const response = await fetch(endpointBase + endpoints["chatEndpoint"], {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({messae: message, attachment: attachment})
    });
    const content = await response.json();
    console.log(content)
}

setUp()