import { fetchWrapper, checkAuthStatus, redirectToLogin } from "./utils.js"
import { ChatWidget } from "./components/ChatWidget.js";
import  config  from "./config.js";

interface PublicUser {
    email: string
}

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

async function chatWidgetCallBack(text: string) {
    const lmReply: Record<string, string> = await fetchWrapper(
        '/chat',
        "GET",
        {},
    )
}

function addChatWidget() {
    const chatWidgetCont = document.querySelector(".chat-widget-cont") as HTMLDivElement;
    const chatWidgetObj = new ChatWidget(chatWidgetCont, '20rem', '30rem', chatWidgetCallBack);
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
    addChatWidget();
}

setUp();