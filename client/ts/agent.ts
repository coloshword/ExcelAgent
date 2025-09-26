import { checkAuthStatus, redirectToLogin, setQueryParam } from "./utils.js"
import { ChatWidget } from "./components/ChatWidget.js";
import { GridWidget } from "./components/GridWidget.js";
import type { FileData } from "./models.js";
import  config  from "./config.js";

interface PublicUser {
    email: string
}

interface TaskResult {
    task_id: string
    task_status: string 
    task_result: TaskResultSheetObject
}

interface TaskResultSheetObject {
    sheet_status: string[][]
    finish_reason: string
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
 * Function updates the task result when finished in the backend 
 * 
 */
function updateTaskResult(resultResponse: TaskResult, addMsgToChatHistory: AddMsg, gridWidget: GridWidget) {
    if (resultResponse.task_result) {
        addMsgToChatHistory(resultResponse.task_result.finish_reason);
        // update the sate of the grid Widget
        //gridWidget.updateGridState(resultResponse.task_result);
        gridWidget.updateGridState(resultResponse.task_result.sheet_status);

    } else {
        console.log("request did not have a task_result")
    }
}

/**
 * Reapeatedly polls the /tasks/ endpoint for the result of the agent task (celery job)
 * @param taskID 
 * @param addMsgToChatHistory: callback function that allows you to add a message to the client chat history. 
 * To be used by the update function post task status is no longer pending
 */
async function pollTaskStatus(taskID: string, addMsgToChatHistory: AddMsg, gridWidget: GridWidget) {
    let intervalID: number | null = null;
    async function pollTaskStatusOnce(taskID: string) {
        const endpoint = `${config['server_uri']}/tasks/${taskID}`
        try {
            const response = await fetch(endpoint, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                },
            })
            const content = await response.json()
            if (content.task_status != 'PENDING' && intervalID != null) {
                // clear the interval since its done 
                clearInterval(intervalID);
                updateTaskResult(content, addMsgToChatHistory, gridWidget)
            }
        } catch (error) {
            console.log(error);
        }
    }

    // set interval to 
    const pollingFrequency = 3000; // poll every 3 seconds
    intervalID = setInterval(pollTaskStatusOnce, pollingFrequency, taskID)
}

/**
 * Factory to create callbacks for chatWidget
 * @param addMsgToChatHistory 
 */
function makeChatWidgetCallback(addMsgToChatHistory: AddMsg, datagridWidget: GridWidget) {
    return async function chatWidgetCallback(msg: string, attachments: FileData[]) {
        const currentGridData = datagridWidget.getGridData()
        const endpoint = `${config['server_uri']}/agent_request`;
        try {
            const response = await fetch(endpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "user_msg": msg,
                    "sheet_status": currentGridData
                })
            });
            const content = await response.json();
            // set the query parameter to be the value of content 
            // this creates a taskID
            const taskID: string = content.task_id;
            // wait until task_status is finished...
            const taskResult = await pollTaskStatus(taskID, addMsgToChatHistory, datagridWidget);
        } catch (error) {
            console.log(error);
        }

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
 * setups event listeners for the sheet selector modal
 */
function activateSheetSelectorModal() {
    console.log("this was called")
    const createNewSheetBtn = document.querySelector(".create-new-sheet-btn") as HTMLButtonElement;
    createNewSheetBtn.addEventListener('click', () => {
        const sheetSelectorModal = document.querySelector(".sheet-selector-modal") as HTMLDivElement;
        sheetSelectorModal.classList.add('hidden');
        console.log("create new sheet called");
    });
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
    activateSheetSelectorModal;
}

setUp();