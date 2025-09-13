import { checkAuthStatus, redirectToLogin, setQueryParam } from "./utils.js"
import { ChatWidget } from "./components/ChatWidget.js";
import { GridWidget } from "./components/GridWidget.js";
import type { FileData } from "./models.js";
import  config  from "./config.js";

interface PublicUser {
    email: string
}

type AddMsg = (text: string) => void;


/**
 * function to display the authenticatedResource
 * Only to be called when user is authenticated
 * Params:
 *  user: the PublicUser object 
 */
function displayAuthenticatedResource(user: PublicUser) {
    const usernameDisplay = document.querySelector(".username-disp") as HTMLSpanElement;
    const authDisplay = document.querySelector(".auth-display") as HTMLDivElement;
    authDisplay.classList.remove("hidden");
    usernameDisplay.innerText = user.email;
}


/**
 * Factory to create callbacks for chatWidget
 * @param addMsgToChatHistory 
 */
function makeChatWidgetCallback(addMsgToChatHistory: AddMsg, datagridWidget: GridWidget) {
    return async function chatWidgetCallback(msg: string, attachments: FileData[]) {
        const currentGridData = datagridWidget.getGridData()
        const endpoint = `${config['server_uri']}/agent_state`;
        const response = await fetch(endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "agent_messages": [{"role": "user", "content": msg}],
                "sheet_status": currentGridData
            })
        });
    };
}

function addChatWidget(dataGridObj: GridWidget) {
    const chatWidgetCont = document.querySelector(".chat-widget-cont") as HTMLDivElement;
    const addMsgToChatHistory: AddMsg = (text:string) => {
        chatWidgetObj.addMsgToChatHistory(text)
    }
    const chatWidgetCallback = makeChatWidgetCallback(addMsgToChatHistory, dataGridObj);
    const chatWidgetObj = new ChatWidget(chatWidgetCont, '20rem', '30rem', chatWidgetCallback);
}

/**
 * Adds the datagrid to the DOM
 */
function addDataGrid() {
    const dataGridCont = document.querySelector(".datagrid-cont") as HTMLDivElement;
    const dataGridObj = new GridWidget(dataGridCont);
    return dataGridObj;
}

/**
 * set up function to be called at window load time 
 */
async function setUp() {
    // check if auth
    const userOrNull = await checkAuthStatus();
    if (! userOrNull) {
        redirectToLogin()
    }
    // cast userOrNull
    const publicUserObj = userOrNull as PublicUser;
    displayAuthenticatedResource(publicUserObj);
    const dataGridObj = addDataGrid();
    addChatWidget(dataGridObj);
}

setUp();