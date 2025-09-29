import { checkAuthStatus, redirectToLogin, setQueryParam } from "./utils.js"
import { ChatWidget } from "./components/ChatWidget.js";
import { GridWidget } from "./components/GridWidget.js";
import type { FileData, ModifySheetsIn, ModifySheetsOut, Sheet } from "./models.js";
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

// caching common items 
const sheetSelectorModal = document.querySelector(".sheet-selector-modal") as HTMLDivElement;

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
                credentials: "include",
                mode: "cors",
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
                credentials: "include",
                mode: "cors",
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
 * dataGridObj: the GridWidget element to get the current state of the sheet 
 */
function activateSheetSelectorModal(dataGridObj: GridWidget) {
    const createNewSheetBtn = document.querySelector(".create-new-sheet-btn") as HTMLButtonElement;
    const gridData = dataGridObj.getGridData()
    createNewSheetBtn.addEventListener('click', async () => {
        // make a request to create a new sheet 
        const endpoint = `${config['server_uri']}/sheets`;
        const payload: ModifySheetsIn = {
            sheet_name: "Untitled",
            sheet_status: gridData
        }
        const res = await fetch(endpoint, {
            method: "POST",
            credentials: "include",
            mode: "cors",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });
        const data: ModifySheetsOut = await res.json();
        if (data.sheet_id) {
            setQueryParam("sheet_id", String(data.sheet_id));
            sheetSelectorModal.classList.add('hidden');
        }
    });
}

/**
 * setups event listeners for the header functions
 */
function activateHeaderFunctions(dataGridObj: GridWidget) {
    const saveBtn = document.querySelector(".save-btn") as HTMLButtonElement;
    saveBtn.addEventListener('click', async () => {
        const gridData = dataGridObj.getGridData();
        const url = new URL(window.location.href);
        const sheet_id = url.searchParams.get('sheet_id');
        if (! sheet_id) {
            return;
        }
        const endpoint = `${config['server_uri']}/sheets/${sheet_id}`
        const payload: ModifySheetsIn = {
            sheet_name: "Untitled",
            sheet_status: gridData
        }
        const res = await fetch(endpoint, {
            method: "PUT",
            credentials: "include",
            mode: "cors",
            headers: {
                "Content-Type": "application/json"
            },
            body : JSON.stringify(payload)
        });
        const data: ModifySheetsOut = await res.json();
        console.log(data);
    });
}

/**
 * displaySavedSheets: display the user's previous sheets
 */
async function displaySavedSheets(dataGridObj: GridWidget) {
    const endpoint = `${config['server_uri']}/sheets/getUserSheets`
    const res = await fetch(endpoint, {
        method: "GET",
        credentials: "include",
        mode: "cors",
        headers: {
            "Content-Type": "application/json"
        },
    })
    const data: Sheet[] = await res.json();
    const container = document.querySelector(".sheet-selector-modal-sheet-container") as HTMLDivElement;
    for (var i = 0; i < data.length; i++) {
        // create sheet container link 
        const sheet = data[i] as Sheet;
        const sheetSelection = document.createElement('div');
        sheetSelection.classList.add("sheet-selector-modal-sheet-selection");
        const sheetNameSpan = document.createElement('span');
        sheetNameSpan.innerText = data[i]!.sheet_name;
        const lastUpdatedTimeSpan = document.createElement('span');
        const lastUpdatedTimeDate = new Date(data[i]!.last_update_time)
        lastUpdatedTimeSpan.innerText = lastUpdatedTimeDate.toString();
        sheetSelection.appendChild(sheetNameSpan);
        sheetSelection.addEventListener('click', () => {
            loadSavedSheet(sheet, dataGridObj);
        });
        sheetSelection.appendChild(lastUpdatedTimeSpan);
        container.appendChild(sheetSelection)
    }
}

/**
 * event listener to display a saved sheet 
 * @param sheet 
 * @param gridWidgetObj: the grid widget instance 
 */
function loadSavedSheet(sheet: Sheet, gridWidgetObj: GridWidget) {
    // do two things, set the query param to the item, and set the grid state to the sheet data 
    gridWidgetObj.updateGridState(sheet.sheet_status);
    sheetSelectorModal.classList.add('hidden');
    setQueryParam("sheet_id", String(sheet.id));
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
    activateSheetSelectorModal(dataGridObj);
    activateHeaderFunctions(dataGridObj);
    displaySavedSheets(dataGridObj);
}

setUp();