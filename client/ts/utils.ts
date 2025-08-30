// utils.ts: random utility functions 
import config from "./config.js";

/**
 * Light wrapper for fetch. Must be awaited. Use Try, catch as well
 * Params:
 *  endpoint: the endpoint to fetch from, not including the base 
 *  requestMethod: the request method to use (POST, GET, etc...)
 *  params: the object with all Parameters
 * 
 */
export async function fetchWrapper<T>(endpoint: string, requestMethod: string, params: object | null=null, includeCredentials:boolean=true): Promise<T>{
    const endpointBase:string = config['server_uri'];
    const requestObject: RequestInit = {
        method: requestMethod,
        mode: "cors",
        headers: {'Content-Type': 'application/json'}
    }
    if (includeCredentials) {
        requestObject["credentials"] = "include"
    }
    if (params) {
        // add body with JSON.stringify
        requestObject["body"] = JSON.stringify(params);
    }
    const fullEndpoint = `${endpointBase}${endpoint}`
    // make the request 
    try {
        const response = await fetch(fullEndpoint, requestObject);

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response}`);
        }
        const res = await response.json();
        return res;
    } catch (error) {
        console.log(error);
        throw error; // propagate error for outer layer try catch
    }
}


/**
 * Function to check the auth status
 * @returns user object if authenticated || null if not authenticated 
 */
export async function checkAuthStatus() {
    try {
        return await fetchWrapper("/users/me", "GET")
    } catch (error){
        console.log("Auth check failed:", error);
        return null; // null if not auth
    }
}

/**
 * Function to redirect back to the login page 
 */
export function redirectToLogin() {
    const loginURI = `${config["client_uri"]}/login_with_google.html`;
    window.location.href = loginURI;
}

/**
 * Function to set queryParam
 */
export function setQueryParam(paramName: string, paramValue: string) {
    const url = new URL(window.location.href);
    url.searchParams.set(paramName, paramValue)
    window.history.replaceState( {paramValue}, "", url);
}