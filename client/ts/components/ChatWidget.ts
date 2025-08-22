//chatInterface.ts: the reusable web component to display the chatInterface 

/**
 * ChatWidget: defines a chat interface as a component
 */
export class ChatWidget {
    private parent: HTMLElement;
    private width: string;
    private height: string;
    /**
     * The constructor for ChatWidget
     * @param parent: the parent element to attach the chatWidget to 
     */    
    constructor (
        parent: HTMLElement,
        width: string,
        height: string
    ) {
        this.parent = parent;
        this.width = width;
        this.height = height;
        this.init();
    }

    /**
     * sets up the html skeleton to the DOM
     */
    private toDOM() {
        const htmlContent =`
            <div class="chat-widget-chat-widget">
                <span>This is the chat widget</span>
                <input type="text"/>
            </div>
        ` 
        this.parent.innerHTML = htmlContent;
        const widget = document.querySelector(".chat-widget-chat-widget") as HTMLDivElement;
        widget.style.setProperty("--chat-width", this.width);
        widget.style.setProperty("--chat-height", this.height);
    }

    /**
     * addUserMessage: adds the user message.
     */

    /**
     * the init function 
     */
    private init() {
        this.toDOM();
    }
}