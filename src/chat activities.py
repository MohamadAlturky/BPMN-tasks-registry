import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama

load_dotenv(override=True)

llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))

process_description = "Consider a process for purchasing items from an online shop. The user starts an order by logging in to their account. Then, the user simultaneously selects the items to purchase and sets a payment method. Afterward, the user either pays or completes an installment agreement. Since the reward value depends on the purchase value, After selecting the items, the user chooses between multiple options for a free reward. this step is done after selecting the items, but it is independent of the payment activities. Finally, the items are delivered. The user has the right to return items for exchange. Every time items are returned, a new delivery is made."

PROMPT="""
In Business Process Model and Notation (BPMN), a task is a self-contained activity that represents a piece of work to be performed within a process. Here are some common types of tasks in BPMN:

**Types of Tasks:**

1. **Service Task**: A service task represents an action or operation that can be invoked as a service, such as a database query, a web service call, or an external system interaction.
2. **User Task**: A user task represents a step where a human participant is required to perform some work, such as filling out a form or making a decision.
3. **Script Task**: A script task allows you to execute a small piece of code or a script within the process. This can be useful for automating specific tasks or performing complex calculations.
4. **Manual Task**: A manual task represents a step where no automation is possible, and human intervention is required.     

Extract the tasks with it's types in this process description:
```
{process_description}
```

** Output structure **:
is a list of this formate
`
task name
task type
task description
`
**Notes**:
- make the names of tasks short and consice.
"""
llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))

complete_prompt = PROMPT.replace("{process_description}", process_description)

generate = llm.invoke(complete_prompt)

print(generate)
print()
print()
print()
print()

PROMPT = """
as a json expert represent the given tasks in a json list.

**Expected output**:
a valid json list object of this formate 
{
    "name":"string",
    "type":"string",
    "description":"string",
}

**The tasks**
{tasks}

**Notes**:
write the json inside a section of this formate

```json
the json object
```

"""
llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))

complete_prompt = PROMPT.replace("{tasks}", generate)

generate = llm.invoke(complete_prompt)

print()
print()
print()
print()
print()
print(generate)
print()
print()
print()
print()