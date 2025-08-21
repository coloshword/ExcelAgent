import { fetchWrapper, checkAuthStatus } from "./utils.js"

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

/**
 * 
 */
function displayNotAuthenticated() {
    const notAuth = document.querySelector(".not-auth-display") as HTMLDivElement;
    notAuth.classList.remove('hidden');
}

/**
 * set up function to be called at window load time 
 */
async function setUp() {
    // check if auth
    const userOrNull = await checkAuthStatus();
    if (userOrNull) {
        // cast userOrNull
        const publicUserObj = userOrNull as PublicUser;
        displayAuthenticatedResource(publicUserObj);
    } else{
        displayNotAuthenticated()
    }
     
}

setUp();