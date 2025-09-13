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

    - make a call to the openai api --> through celery worker 
        - write a function to make a request to the LLM with some input text 

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