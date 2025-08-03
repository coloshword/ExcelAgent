/** restrictedPage.ts */
const endpointBase: string = "http://127.0.0.1:8000";

async function setUp() {
    /** request  */
    const displayUserInfo = document.querySelector('.display-user-info') as HTMLSpanElement;
    // make a fetch call for restricted content 
    let displayText = "";
    try {
        const response = await fetch(endpointBase + "/protected", {
            method: "GET",
            mode: "cors",
        });
    
        if (!response.ok) {
            console.log(response)
            throw new Error("http error");
        }
        const res = await response.json();
        console.log(res);
    } catch (error) {
        displayText = "You are unauthorized";
    }
    displayUserInfo.innerText = displayText;
}

setUp();