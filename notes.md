-- code everday
    - spreadsheet ai full stack app

-- interview prep
    - leetcode
    - system design

-- job apps 
    - 10x a day

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
- tasks: function with the @task decorator. Such a function is told to run asynch
- workers: worker processes the queued task in the background.
- brokers: after task creation, celery sends it to a broker to be queued. Intermediary that handles message passing between two... something like redis
    - Redis: stores things in memory as key-value, (not disc) so fast

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


- AsyncResult() --> object allows you to monitor the status of a task, given the task_id used to create it 
