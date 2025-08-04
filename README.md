reminders:
- start the fastapi server:

python -m fastapi dev server/server.py

- test if an endpoint works
- endpoint works,
- let's make the endpoint point to the llm with a chat 
- add a payload, and have it return thep payload?

- so in fast api we need pydantic to define a type, and create that type 
    - let's use types
- so what would my type be
- message, would simply be of type string?
- I guess we would need to include attachment, which can be none, an optional parameteer

- make a request using curl
    - how to make a request using curl?

-X sets the http request method 
-H for the header of the content-type header of the http request to application/json (for json type)
-d used to specify the paylod 

curl -X POST -H 'Content-Type: application/json' -d '{"message":"hello gpt god, what is your name", "attachment":"here is a fake attachment"}' http://127.0.0.1:8000/chat

- endpoint works, now let's make it from the frontend 
- we will simply console.log the output 

- use the fetch API, global function called fetch().
- take the URL as a param
- async, so we return a promise. We can either use a then(), or await. Await in an async function is non blocking, but it does block execution of the code in the function until the promise is returned 
- for the sake of what we are doing, we will simply use .then()

- with the make request function, we are close to making the request. we want to make the request to our python api, and just console log it 

- fixed the issue of the chat, let's have it just print out the resp 
- point it to the gemini endpoint 

## postgresql quick start
- use client/server model (spin up a server process during the start)
- database server program is called `postgres`
+--------+       HTTP    .     +---------------------+       API Calls / DB Ops      +--------------------+
| Client | <-----------------> | FastAPI Server      | <---------------------------> | PostgreSQL Database|
| (Web   |                     | (Stateless Process) |                               | (Agent State, DFs) |
| Browser)|                    |                     |                               +--------------------+
+--------+                     |                     |                                         ^
                               |  1. Receives Request|                                         |
                               |  2. Retrieves Agent |                                         |
                               |     State from DB   |                                         |
                               |  3. Calls Gemini API|                                         |
                               |     (I/O-Bound)     |                                         |
                               |  4. Dispatches CPU- |                                         |
                               |     Bound `exec()`  |                                         |
                               |     Task to Broker  |                                         |
                               |  5. Returns Response|                                         |
                               |     (or Task ID)    |                                         |
                               +---------------------+                                         |
                                         |                                                     |
                                         |  (Asynchronous Task Dispatch)                       |
                                         V                                                     |
                               +---------------------+                                         |
                               | Celery Message      |                                         |
                               | Broker (e.g., Redis)|                                         |
                               +---------------------+                                         |
                                         |                                                     |
                                         |  (Task Consumption)                                 |
                                         V                                                     |
                               +---------------------+                                         |
                               | Celery Workers      | <---------------------------------------+
                               | (CPU-Bound Python   |  (Access DB for state, save results)
                               |  Execution, `exec()`) |
                               +---------------------+

### db ops
- created first table, populated with an entry
- start using python to query 
- successfully queried a table from python using postgres

- next thing: we need a session id
- why? session id will be used to reference dataframes and other important information. 
- save it in the db, so that we will not have to remember anything in the server, actual execution server is stateless 

## creating basic auth
- jwt: used for auth by generating the token upon user login, and then use it for subsequent requests 

- oath2: authorizaotion framework
- use passlib for hashing passwords 

- httpBasic(), creating a protected endpoint, by giving an endpoint Depends(auth_function), where the auth function depends on httpBasic

- auth fn acts as middleware (reminder: mdware being the layer that runs before your endpoint)
- client - middleware - route - middleware - response - client 

- CryptContext --> handles secure password hashing and verification 
    - hashes the password (hash = pwd_context.hash("some password))
    - also verifies against hashes (pwd_context.verify(<user input>, stored_hash))

- OAuth2PasswordBearer: prepares JWT token authentication 

NEXT: 
add fake db and password functions 
- now we are adding user lookup and authentication functions 
- login flow:
    - we run authenticate user, which provides a db, username, and password
    - authenticate_user() calls get_user() which either returns None or 
    a UserInDB object, which is just a Pydantic User object with an extra field hashed_password
    - if get_user() returns None, then we return False (it doesn't exist)
    - if user exists, get_user() creates a UserInDB object, using ** to unpack a dictionary. Make sure keys match.
    - the UserInDB object represents the "ground-truth" object of the user's authentication -- it is pulled straight from the db with the hashed_password to create the UserInDB object
    - returning the UserInDB model, we can now use it as any regular object, in which case we use it to veriy_password by comparing the login provided password with the user's hashed_password 
    - we separate UserInDB and User, as UserInDB is sensitive information, representing the User with the hashed password, while User is just typical information we can display to the frontend. If we wanted to send the information to the frontend, all we have to do is cast it to a User and send.

### jwt's 
- now we add jwt 
    - jwt contains all the user information needed so used by auth
    - string followed by header.payload.signature
    - header says algorithmn and token type 
    - payload contains claims (username, exp)
    - signature is a hash to verify no tampering 
    
    timeline:
    - user logs in --> server creates a jwt and sends it to the client 
    - client stores jwt in localStorage or cookie 
    - for all furture requests requiring auth --> client sends JWT in the "Authorization" header 
    - server verifies the signature and reads payload 

    - our function in auth.py server side: creates a jwt token with expiration time expires_delta
    - we use jose.jwt to encode, using secret_key and algorithmn. secret_key is some string used to encode our data, and is needed to decode the encoded jwt token 

- working on some token validation functions (used to take our jwt and read it essentially)
    - used to continuously check access 
    - jwt.decode(token) would throw some sort of error if tampered, if the payload is decoded successfully, and you can access the payload for a username, you are good, this is a valid jwt token

- work on adding the auth endpoint 
- after login, we get a JWT.
- accessing get_current_user() function requires a JWT token to be given access, otherwise access won't be granted 

### token 
/token endpoint accepts username and password, returning a jwt token.

/users/me endpoint get's the user's information using the token 

/docs --> just some sample ui to test endpoints interactively -- including auth.
- after doing "Authorize", it sends the jwt to all protected routes.

## login page 
- set up basic login page
- next thing, make the login page request a jwt token
- what's the endpoint for this? 
- endpoint is login_for_access_token
    - need to findout, what the heck is form_data 
    - payload seems to be: 
    {
        "username":
        "password":
    }
    - so we make a request using this?
    - use fetch api again

    body is gonna be: 
    {
        "username":
        "password":
    }
    - you gotta use FormData() and not json.

- 422 code "Unprocessable Entity" means server understood your request, but could not process it due to semantic error 
- in my case, I did FormData as the payload, but I gave it a "Content-Type": "application/x-www-form-urlencoded" in the header, which explicitly set the body to www-form-urlencoded format. So the server is confused, since the body is "multipart/form-data" format, but I said its urlencoded format -- hence the error. By not setting the Content-type to anything explicit, the browser handled it on its own, and set it automatically so it worked.

- now that I generate the jwt token properly, we need to figure out how to store it in the client, and also how to use it for further auth. 

### adding jwt to client 
- after receiving the jwt from the server, we want to store it in the client (browser). And the client then uses this jwt token in the authorization header when making requests to the server that require auth 
- well just use cookies since it seems to be the easiest -- less vulnerable to xss attacks 
- remember to use httponly flag 
- so can't be done on the client using javascript, because xss attack, a script can get the cookie and impersonate
- store cookie in a HTTPOnly cookie 
    - prevents client side js (even with XSS attack) steals the JWT token 
    - also does automatic handling. Once token is in an HttpOnly cookie, browser auto attaches it to every subsequent request to the same domain. Simplifies client side code 

- instead of a client-side fetch request returning the JWT in the response body, server set the HttpOnly cookie directly in the response header. The server's response to the login request would contain a Set-Cookie header. The browser recieves this header, and auto stores the cookie, bypassing the need for client code to explicit this. 
    - in short: client side code doesn't even reference the cookie 
    - server tells the browser to "remember" this jwt token for all future requests to the domain (by doing a Set-Cookie header)

- trick: use dependency injection in fastapi. When you need to use a certain object like the FastAPI.Response() class, just add it to the parameter list, and refer to it in the code. You don't need to provide it when calling the function, FastAPI creates one for you.
    - inject the Response object, to manipulate the headers like (Set-Cookie header), but still return the original dictionary to provide the response body to be serialized to json

- created a restricted page: now we will load the resource seeing if it has access to it.

- working on: a sample page that will show restricted content only to authenticated users.
    - why is the restricted client page not able to access the protected content despite jwt token being added to the browser using the Set-Cookie header? 
        - because cors, since our client and server are different ports, it's a cross origin request, and fetch-api by design does not send credentials (like cookies and auth headers) with cross origin requests
            - key? include:
                credentials: 'include' in the fetch call
        - well that did not fix the issue... let's make sure that set-cookie is indeed setting the cookie 

        - the source of the bug: not setting a location for the Set-Cookie header. I used Set-Cookie, but didn't provide a location, so the browser by default associated my jwt cookie with the origin of the page that made the request, (client code running on 5500). however, server is on port 8000. Hence when I told it to include the authorization , the browser just didn't send the jwt token in the authorization header since it saw that we are making a request to port 8000, but the jwt cookie is supposed to be used only to localhost:5500. Server then receives the get request with no authorization header hence ==> not authorized. 
        - so the idea: use dependency injection to see the HOST of the request, aka (the server the http request is being sent to). This way, I dynamically know what the ip and port is the server is running on (as it can change if its hard coded). 
            - use the set_cookie, with domain to get the actual domain. 