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

- we now have the user info 

- users table is created
- let's create the users on login
- write some simple code to create a user... 
- and some simple code to get a user 
- this will take the SimpleConnection Pool to do this


- create user is created, now for login user 
- let's add create user to the server endpoint 

- is_user_in_db: works 

- now we need to set the jwt... how do we do that 
we can do depedency injection  using response.set_cookie

### auth pattern

- a protected page should immediately make a call to something like:

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(auth.get_current_active_user)):
    """Get current user information."""
    return current_user

    - return 200: render the agent ui, & show user info (optionally!)
    - 401? : show "unauthorized", link to login, and don't show any other data


- work on creating a protected page...

- for using pool.getconn(), make sure to use pool.putconn() to restore the connection

- using Depends() --> your function needs a specific value for a parameter, and you have a function that allows you to get it, you can define the parameter as Depends() on the function that gives you that value, and fastapi chains that function to be called to give you that value 

- now to work on created page,
- we should redirect after applying the cookie 

- we are going to assume there's nothing wrong with the cookie.

- that means we will just request from the endpoint as intended.

- we seemed to have solved the problem of redirects, we found the right location..., the issue is that validation is failing at some point
    - we do have an access_token...
    let's see what is wrong with users.me
    - users/me calls get_current_user() from auth... 
    - we are making it all the way to the auth.get_user() call 
    - oh yeaaa auth works baby, we are getting auth!
    - let's have it return "PublicUser" information
        - for now we'll just have it return email
        - ok let's display the email now, since it will 100% be in json

make restrictedPage allow either interaction with agent or not. 
Conditional 
- (not auth): You have to login to access the agent 
            <login with google> flow 

- if (auth): show the agent

- some typescript perculiarity: 
    RequestInit -- > ts type definition of anything you pass fetch to

- async / await functions, return type you gotta wrap Promise<type> for it.

- work on redirect back to login with google 
    - redirect use window.location.href = <uri>
### Aug 22
- finish the chat component 
    - work on adding a callback function in the constructor

    
- hook it up to an LLM endpoint 
- for our web component, make sure to just query this.parent, instead of document.querySelector
this way our web component is encapsulated 
- importance of arrow methods --> this normally refers to the thing that called the function, but in the case where we are creating the web component as a class, we want this() to refer to the object as a whole, so we make it an arrrow function 


### Aug 23:
- finish the chat component 
    - callback function should hook up to an endpoint that spews out LLM chat
    - callback function should call an endpoint
    - server should make a request to an LLM
        - return that content to the frontend interface 
        - LLM is called properly
        - we need to make sure to wall it off with auth, so if you are not authenticated, it shouldn't allow a call
        - now the endpoint only works when authentication exists 
        - now let's make it actually add to the client ! 
        - callback function almost correctly adds to the chat history. Firstly, we are not adding the actual lm output yet, and we also aren't passing in the correct message to the lm input
            - actually add the LM output instead of some generic string
            - ok so now actual LM output is added instead of generic string
            - clean up some of the nesting on this 
            - cleaned up the nesting, ok so now we will work on actually sending the payload properly this time.
                - this means adding params to the actual function
    

- concurrency in the server:
    - i should be chilling as long as all my server code is truly async and non blocking
    - we will use uvicorn in production 
    - holy shit ground breaking: define a endpoint as "sync" and not async in fastapi, and it will automatically offload it to threadpool executor and not stall everyone 

    @app.get("/slow")
    def slow_route():
        time.sleep(5)  # totally blocking
        return {"message": "done"}
    
    - this is safe because it is synchronous, and won't kill people trying to login for 10 seconds, but if we defined it as async it would be a problem. 
    - remember messages is just a list of dicts.
        each dict is of the form:
        {
            "role":
            "content":
        }
    
    - /chat works right now 

    - <T> == type parameter: type placeholder, how you can make a type generic 
    
    so to make a function generic 

    async function fetchWrapper<T>(Params): Promise<T>
        - so not only do you have to type the return as <T>, but you also have to put <T> next to the function name
        - and this changes how you call the function: you have to do <T> next to the function calls to provide the output type 

        const resp = await fetchWrapper<User>(); // for example

        - some more casting 
        (<HTMLInputElement> e.target) --> can cast the element 

        - optional chaining: --> `?`: only access this property if the thing before is not null or undefined, otherwise just return undefined 
        - typing of resolve, reject: it's going to be a Promise type string

-- basic chatting component is done
- now we want to finish including an attachment
- we want to include attachments
- we want to include the attachment button and include the attachment input
- make it a button, and have an invisible input element 
- have an attach button, its going to be the thing that triggers the attachment 


### Aug 24.
- work on the attach button and wire it to the backend 
    - attach button now properly reads the file as b64
    - work on 1. displaying the file as uploaded
        - we need a display updated files list 
        - file list is missing something, it's missing the actual name
        - we want the name to display...
        - so instead of a list of strings, we'll do a list of objects 
        - we are now displaying the file after uploaded using the new interface

    - save it as a state so that we can actually send it in during the send portion of the chat 
        - save it as a state! We will call it an attachments list!
        - state is now saved 

    - update the backend endpoint to include the file upload 
        - working on this now 
        - we need to upload the whole as a optional payload
        - works now!

- if we define an interface, we just use it as a type, you don't instantiate the interface at add time, you create an object that conforms to the interface 

### Aug 25. 
- start implementation of the actual agentic portion 

- next step:
1. Add tasks + Sheet Upload + Preview 
- tasks will represent a task the agent can do, and will be created 
- incur "memory" with the task id as query param 
- "memory", let's do chats with memory 
- keep a persistent "chat" to get, and then we can just pull it 

    Table tasks(task_id, sub, last_activity_at)
    - we should be able to create a new task when triggering a 
    - should we include chat log inside of tasks? 
    - i don't care about chat log for now, we just need to have a way to remember sessions 
    - each user can create a task

### Aug 26. 
    GOAL:
        - TASK does have a chat log, that only makes sense...
        - For now we'll make it attachment only
        - we should be able to create a task when an attachment is made. 
        - and then we should be able to retrieve attachment if its a past task 
        - don't worry about chat log
        - don't worry about "history"
        - simply create a task when a attachment is made 

    - chat right now is an empty thing...
    - how do i make it so that we know from the endpoint whether or not to pull up a chat history?
    - provide a task id 
    - task endpoint creates a new task

    -SQL: REFERENCES --> foreign keys, so REFERENCES tasks(task_id), says that this value in this other table must match a value that exists in the tasks table, specifically it must match a task_id

    - ON DELETE CASCADE --> if the referenced row is deleted, this is deleted as well.

# IMPORTANT TODOS: do not delete this section
- check state in google oath and make sure this can't be spoofed
- create_task should include Idempotency-Key 

# simple idea:
    - create a simple task if attachment is added 
    - simply create a task
