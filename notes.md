-- code everday
    - spreadsheet ai full stack app

-- interview prep
    - leetcode
    - system design

-- job apps 
    - 10x a day

### python -m pytest -c custom_pytest.ini
### 09/13/25
- stores agent_state in db
- store agent_state_id from db value 

- trigger the agentic flow 
    - for a single iteration...
    - heres the agent state 
    - <lm> do something 
    - return new state back to the client 

- chatWidgetCallback --> create the agent state / update it (if it already exists)
    - call the trigger_agent_step() --> one step of the lm (pass in id)
        - do the agentic flow 

### agentic flow 
    - a way to implement task queues outside of the request-response cycle 
    - no agentic flow 
    - user_message --> CELERY --> LLM api call --> return output (server) --> client 
    - task_id is simply agent_state_id
    - docker set up
    - celery & redis are both running on docker

    - make a call to the openai api --> through celery worker  -- done 
        - write a function to make a request to the LLM with some input text -- done 
    - pass in the chat state to the celery worker to make the call
        - chat history is on the client
        - don't expose entire system prompt and everything, so the actual request body with the openai chat completions should be built on the server.
        - ground truth: the db
        - client will "simulate" it
    
    - lm requests must be being made properly... we need to see the redis state 

### Celery main components 
### - tasks: function with the @task decorator. Such a function is told to run asynch
### - workers: worker processes the queued task in the background.
### - brokers: after task creation, celery sends it to a broker to be queued. Intermediary that handles message passing between two... something like redis
### - Redis: stores things in memory as key-value, (not disc) so fast

- declaring a celery task
```python
app = Celery('example_project', broker=<redis location>)
@app.task 
def add(x, y):
    return x+y
```
- this creates a app task 

- to run add asynchronously, call .delay()

```
add.delay(10, 20)
```
**we probably want to retrieve some value**

- localhost inside of a container == that container, not the same as redis container


### 09/14/25 

- deploy with docker ( 3 containers) : redis, celery worker, web component 
- make calls to the llm through the celery worker 
- not : get outputs back to the web component --> back to client 

** Somehow get the LLM api call results to the client ** 
    - LM requests are now using the user input 
    - get the result back to the server...
    - do polling by returning the task_id...
    - agent_state_id --> identifier for the current "chat" history
        - task_id: the current identifier for the last request to the agent...
        - keep updating task_id, but don't update agent_state_id

        - want a request handler for GET/tasks/task_id

        - question: do we implement polling in the chatWidgetCallback?
            --> we probably don't want the user to be able to make any requests while its working, so polling should be in the callback

            - function: takesID, polls every 0.5s, for the result of the task at the endpoint
        
        - GET "tasks/{task_id} is working now 

        - create the polling system on the frontend, and then display the output chat  -- DONE 

 ### AsyncResult() --> object allows you to monitor the status of a task, given the task_id used to create it 
### **Agentic flow**

```python
def trigger_agent_flow(): 
    ## first thing would be to make a new agent state 
    ## create a 40 x 24 grid to represent input data 
    inner_grid = [['' for x in range(24)] for y in range(40)]
    user_request = "Please add the 10 countries with the highest population in the first column"
    # goal: return grid with this back to the frontend, making sure to use celery
```

### goal is to get the celery worker to mock all of this up
agent_worker: the module using celery that will be responsible for all of this
won't make it class based since we want it to be stateless 

- Create the system prompt for this 
- create the tools for tool calling 
- proper tool calling
    - https://ai.google.dev/gemini-api/docs/function-calling?example=meeting


### 09/15/25
- Goal: write the agentic loop 
    - define tools: 
        - execute_code 
        - view_spreadsheet
    - write an entire loop
        - make agentic_request 
            --> celery worker triggers agentic loop
            - "finished"
        - client continuously poll output 
    
    - right now we are just making an agent_worker make a request to the LM.
    - instead we probably want to wrap the whole thing in an agent loop...
        --> rename agent_functions to agent_helper
        --> agent_worker goes back to worker
        --> define a new module "agent.py" --> all agent functions including the main agent loop

### Agentic loop
React --> Reason (think about the tool you need) --> Act (call the tool)

    Tools: 
        - view_sheet(): returns a slice of the sheet as a dataframe view 
        - execute_code(): takes code and executes it
        - Return answer(): stop the agent loop, (while loop) --> flag (done = True)
    
    - Write the system prompt to define these tools 
    - write the tools 
    - write the loop
    - separate reasoning and acting
        - if the last step was reasoning, we want to call acting 
        - at each reason / act step we want to be able to update the status of task_done, in otherwords return
        a boolean if the step is done 
    
    - what would agent_reason actually do? 
        - we would want to let the agent know it is time to reason 

    - make multiple types.Content to define sys prompt

### agent message structure:
    - an important thing to keep in mind is that the "conversation" system should be "user" --> "model" --> "user"
    - if i send two "user" chats at once, it ends up breaking the conversation and we get weird behavior 


- it's going to generate a bunch of tokens, even function call during the reasoning stage. We won't let it reason, until we have it act
    
    **TODO**: If the first step is always agent reason, how do we do init_agent_message_history, and how does taht differ from the agent_reason step?

### 09/16/25
- start of the agent loop (reasoning step --> action step)
    - tool calling using google.genai
    - structure of the tools & what they do
    - 1 (reason -> act) cycle loop 

    - implement the tools 
    - call the agent loop & have it update the client state 

    - should it be 3 or 4 
    
    agent_reason():
        - user request + 1st reasoning step
        - LM response 
        - 1st act step instructions 
        - LM act response 

        = 4 
    
    - call agent_reason and agent_act from celery
        - working from celery worker


### project todos 
1) make the spreadsheet more "spreadsheet" like (auto expanding rows, etc...)

2) some sort of way to allow for search? the agent should be able to search things up

3) Spreadsheet functions (closer to excel)

4) create "history" --> you should be able to see the agent_state and also select from previous sheets

5) ci/cd?

6) add benchmarking?

7) retry mechanism to allow agent to fix its errors 


current:
2) some sort of way to allow for search? the agent should be able to search things up


### 09/18/25:
- add agent internet search feature 


### agent loop rewrite 

def agent_loop():
- defines the main agent loop
- think --> act loop
- when done? --> flag as done, tool to update the state to done = True? with a 6 step limit 
