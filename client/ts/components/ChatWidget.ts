//ChatWidget.ts: the reusable web component to display the chatInterface 
import type { FileData } from "../models"

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
    addAttachmentBtn!:HTMLButtonElement;
    attachmentInput!:HTMLInputElement;
    attachments: FileData[] = [];
    attachmentsDisplay!:HTMLDivElement;
    onSendCallback: (text: string, attachments: FileData[]) => void | Promise<void>;
    /**
     * The constructor for ChatWidget
     * @param parent: the parent element to attach the chatWidget to 
     */    
    constructor (
        parent: HTMLElement,
        width: string,
        height: string,
        onSendCallback: (text: string, attachments: FileData[]) => void | Promise<void>
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
        this.addMsgToChatHistory(msg);
        // call the callback
        this.onSendCallback(msg, this.attachments);
    }

    /**
     * Add a message to the chat History. Public to let users to 
     * @param msg: the message to add 
     */
    public addMsgToChatHistory(msg: string) {
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
     * Reads a file object and return base 64
     * params: file: 
     */
    private fileToBase64(file: File): Promise<string> {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onerror = () => reject(reader.error ?? new Error("read error"));
            reader.onload = () => resolve(reader.result as string);
            reader.readAsDataURL(file);
        })
    }

    /**
     * Displays the uploaded files based on the attachments object 
     */
    private displayUploadedFiles(): void {
        if (this.attachments.length == 0) {
            return;
        }
        // get rid of hidden as there are attachments 
        this.attachmentsDisplay.classList.remove("hidden");
        // remove all children for updates 
        while (this.attachmentsDisplay.firstChild) {
            this.attachmentsDisplay.removeChild(this.attachmentsDisplay.firstChild)
        }
        for (let i = 0; i < this.attachments.length; i++) {
            const attachmentDisplay = document.createElement("div");
            const attachmentFile = this.attachments[i]; // attachmentFile is of type FileData
            const attachmentFilename = attachmentFile?.filename ? attachmentFile.filename : "<No Name file upload>"
            attachmentDisplay.innerText = attachmentFilename;
            attachmentDisplay.classList.add('chat-widget-attachments-display-cell')
            this.attachmentsDisplay.appendChild(attachmentDisplay);
        }
    }

    /**
     * Event listener function to get the input element to add an atachment
     * @param e: the event for the 'click'
     */
    private inputAddAttachment = async (e: Event) => {
        if (!(e.target instanceof HTMLInputElement)) return;
        const file = e.target.files?.[0]; // so we just return null if files is not defined / null! 
        if (!file) return;
        // read the file and update the status
        const fileB64 = await this.fileToBase64(file);
        // get the filename 
        const filename: string = file.name;
        // add the attachment to the list, conforming to the FileData interface 
        this.attachments.push({
            filename: filename,
            fileContent: fileB64
        });
        // update the visuals 
        this.displayUploadedFiles();
    };

    /**
     * Event listener function for the 'add attachment' button
     */
    private handleAddAttachmentBtn = () => {
        this.attachmentInput.click();
    }
    /**
     * sets up the eventListeners
     */
    private setUpEventListeners() {
        this.sendChatBtn.addEventListener('click', this.addUserMsg);
        this.chatInput.addEventListener('keyup', this.handleKeyDown);
        // add attachmentInput file listener to the input file, and then make button press trigger that input
        this.attachmentInput.addEventListener('change', this.inputAddAttachment);
        this.addAttachmentBtn.addEventListener('click', this.handleAddAttachmentBtn);
    }

    /**
     * sets up the html skeleton to the DOM
     */
    private toDOM() {
        const htmlContent =`
            <div class="chat-widget-chat-widget">
                <div class="chat-widget-chat-history"></div>
                <div class="hidden chat-widget-attachments-display"></div>
                <div class="chat-widget-input-cont">
                    <button class="chat-widget-add-attachment-btn">Add attachment</button>
                    <input class="hidden chat-widget-file-input" type="file" accept=".xlsx, .xls, .csv"/>
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
        this.addAttachmentBtn = this.parent.querySelector(".chat-widget-add-attachment-btn") as HTMLButtonElement;
        this.attachmentInput = this.parent.querySelector(".chat-widget-file-input") as HTMLInputElement;
        this.attachmentsDisplay = this.parent.querySelector(".chat-widget-attachments-display") as HTMLDivElement;
    }

    /**
     * the init function 
     */
    private init() {
        this.toDOM();
        this.setUpEventListeners();
    }
}