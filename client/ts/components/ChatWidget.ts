//chatInterface.ts: the reusable web component to display the chatInterface 

/**
 * ChatWidget: defines a chat interface as a component
 */
export class ChatWidget {
    private parent: HTMLElement;
    private width: string;
    private height: string;
    chatInput!: HTMLInputElement;
    sendChatBtn!:HTMLButtonElement;
    chatHistory!:HTMLDivElement;
    onSendCallback: (text: string) => void | Promise<void>;
    /**
     * The constructor for ChatWidget
     * @param parent: the parent element to attach the chatWidget to 
     */    
    constructor (
        parent: HTMLElement,
        width: string,
        height: string,
        onSendCallback: (text: string) => void | Promise<void>
    ) {
        this.parent = parent;
        this.width = width;
        this.height = height;
        this.onSendCallback = onSendCallback;
        this.init();
    }
    /**
     * Function to handle sending of chats. To be used as part of the event listener. we make it an arrow function to always refer to the ChatWidget object 
     */
    private addUserMsg = async () => {
        const msg: string = this.chatInput.value;
        if (!msg) {
            return;
        }
        this.chatInput.value = '';
        // add the msg as a span to the chat history
        // call the callback
        this.onSendCallback(msg);
    }

    /**
     * Add a message to the chat History. Public to let users to 
     * @param msg: the message to add 
     */
    public addMessageToChatHistory(msg: string) {
        const msgSpan = document.createElement("span");
        msgSpan.innerText = msg;
        this.chatHistory.appendChild(msgSpan);
    }

    /**
     * Function to handle pressing enter on the input 
     * @param e: The Keyboard Event 
     */
    private handleKeyDown = (e: KeyboardEvent) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            this.addUserMsg();
        }
    };

    /**
     * sets up the eventListeners
     */
    private setUpEventListeners() {
        this.sendChatBtn.addEventListener('click', this.addUserMsg);
        this.chatInput.addEventListener('keyup', this.handleKeyDown);
    }

    /**
     * sets up the html skeleton to the DOM
     */
    private toDOM() {
        const htmlContent =`
            <div class="chat-widget-chat-widget">
                <div class="chat-widget-chat-history"></div>
                <div class="chat-widget-input-cont">
                    <input id="chat-widget-msg-input" type="text" class="chat-widget-input"/>
                    <button class="chat-widget-send-chat-btn">Send</button>
                </div>
            </div>
        ` 
        this.parent.innerHTML = htmlContent;
        const widget = this.parent.querySelector(".chat-widget-chat-widget") as HTMLDivElement;
        widget.style.setProperty("--chat-width", this.width);
        widget.style.setProperty("--chat-height", this.height);
        // cache common elements 
        this.chatInput = this.parent.querySelector(".chat-widget-input") as HTMLInputElement;
        this.sendChatBtn = this.parent.querySelector(".chat-widget-send-chat-btn") as HTMLButtonElement;
        this.chatHistory = this.parent.querySelector(".chat-widget-chat-history") as HTMLDivElement;
    }

    /**
     * the init function 
     */
    private init() {
        this.toDOM();
        this.setUpEventListeners();
    }
}