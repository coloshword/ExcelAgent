//login page 
const endpointBase = "http://127.0.0.1:8000";

const loginWithGoogleBtn = document.querySelector(".login-with-google");
/**
 * function to login with google 
 * Called by the login with google event listener
 */
async function loginWithGoogle() {
    try {
        // do not use fetch, RedirectResponse returns a status code and tells the browser to redirect, so it won't have any json
        window.location.href = endpointBase + "/google";
    }
    catch (error) {
        throw error;
    }
}

function setUp() {
    loginWithGoogleBtn?.addEventListener('click', loginWithGoogle);
}

setUp();