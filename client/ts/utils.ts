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
export async function fetchWrapper(endpoint: string, requestMethod: string, params: object, includeCredentials:boolean=true): Promise<object>{
    const endpointBase:string = config['server_uri'];
    const requestObject: RequestInit = {
        method: requestMethod,
        mode: "cors",
    }
    if (includeCredentials) {
        requestObject["credentials"] = "include"
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
        throw error; // propagate error for outer layer try catch
    }
}


/**
 * Function to check the auth status
 * @returns user object if authenticated || null if not authenticated 
 */
export async function checkAuthStatus() {
    try {
        return await fetchWrapper("/users/me", "GET", {}, true);
    } catch (error){
        console.log("Auth check failed:", error);
        return null; // null if not auth
    }
}