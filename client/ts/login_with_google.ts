//login page 

const loginWithGoogleBtn = document.querySelector(".login-with-google");
/**
 * function to login with google 
 * Called by the login with google event listener
 */
function loginWithGoogle() {
    console.log("clicked continue with google");
}

function setUp() {
    loginWithGoogleBtn?.addEventListener('click', loginWithGoogle);
}

setUp();