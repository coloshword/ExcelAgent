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
