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