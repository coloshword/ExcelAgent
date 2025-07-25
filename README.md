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