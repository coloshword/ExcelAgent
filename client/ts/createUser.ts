/** script for the createUser page */
// cache common objects
const loginBtn = document.querySelector(".redirect-login-page-btn") as HTMLButtonElement;
const createUserBtn = document.querySelector(".create-user-btn") as HTMLButtonElement;
const userNameField = document.querySelector(".user-name-field") as HTMLInputElement;
const pswdField = document.querySelector(".password-field") as HTMLInputElement;

/**
 * function to redirect to the login page. To be used in conjunction with an event listener
 */
function redirectLoginPage() {
    window.location.href = "/client/login.html";
}

/**
 * function to create a user. Fn to be called on the event listener for createUserBtn. 
 */
async function createUser() {
    const typedUsername: string = userNameField.value;
    const typedPswd: string = pswdField.value;
    userNameField.value = '';
    pswdField.value = '';
}

/**
 * calls the create user endpoint on the backend to create a user.
 * @param typedUsername: the username that was typed in
 * @param typedPswd: the password that was typed in
 * @return add later 
 */
async function createUserInDB(typedUsername: string, typedPswd: string) {
    try {

    } catch(error) {
        throw error;
    }
}

/**
 * function responsible for setting up event listeners
 */
function setUpEventListeners() {
    loginBtn.addEventListener('click', redirectLoginPage);
    createUserBtn.addEventListener('click', createUser);
}

/**
 * the setUp function
 */
function setUp() {
    setUpEventListeners();
}

setUp();