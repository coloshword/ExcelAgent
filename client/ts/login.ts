/** login.ts: ts for the login page */
// cache common dom elements 
const loginBtn = document.querySelector(".login-btn") as HTMLButtonElement;
const userNameField = document.querySelector("#login-username-input") as HTMLInputElement;
const pswdField = document.querySelector("#login-pswd-input") as HTMLInputElement;
const endpointBase: string = "http://127.0.0.1:8000";

/**
 * function to login. Fn to be called on the event listener for the loginBtn. Handles calling authentication function, and notifying the user of outcome.
 */
async function login() {
    const typedUsername: string = userNameField.value;
    const typedPswd: string = pswdField.value;
    userNameField.value = '';
    pswdField.value = '';
    const jwt = await authenticateUser(typedUsername, typedPswd);
    console.log(jwt);
}

/**
 * Authenticates the user by requesting a jwt token from the server 
 * @param typedUsername: the username that was typed in
 * @param typedPswd: the password that was typed in 
 * @returns 
 */
async function authenticateUser(typedUsername: string, typedPswd: string): Promise<string> {
    try {
        // create the form data 
        const formData = new FormData();
        formData.append("username", typedUsername);
        formData.append("password", typedPswd);

        const response = await fetch(endpointBase + "/token", {
            method: "POST",
            mode: "cors",
            body: formData,
        });

        if (!response.ok) {
            console.log(response);
            throw new Error(`HTTP error, status: ${response.status}`)
        }

        const res = await response.json();
        return res.access_token;
    } catch (error) {
        throw error
    }
}


/**
 * Sets up the event listeners
 */
function setUpEventListeners() {
    loginBtn.addEventListener('click', login)
}

/**
* set up function 
*/
function setUp() {
    setUpEventListeners()
}

setUp()