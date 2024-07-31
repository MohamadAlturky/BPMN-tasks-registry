import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama

load_dotenv(override=True)

llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))

process_description = "Consider a process for purchasing items from an online shop. The user starts an order by logging in to their account. Then, the user simultaneously selects the items to purchase and sets a payment method. Afterward, the user either pays or completes an installment agreement. Since the reward value depends on the purchase value, After selecting the items, the user chooses between multiple options for a free reward. this step is done after selecting the items, but it is independent of the payment activities. Finally, the items are delivered. The user has the right to return items for exchange. Every time items are returned, a new delivery is made."

PROMPT="""
In BPMN (Business Process Model and Notation), Events represent occurrences that affect the execution of a process. They can 
be either internal to the process or external to it, but they all have an impact on how the process behaves.

There are three main categories of Events in BPMN:

1. **Start Events**:
        * Represent the starting point of a process.
        * There are four types of start events: Message Start Event, Timer Start Event, Conditional Start Event (also known as Exclusive Choice), and Multiple Instance Start Event.
2. **Intermediate Events**:
        * Occur within a process flow and do not affect the sequence flow directly.
        * There are three types of intermediate events: Error Intermediate Event, Compensation Intermediate Event, and Cancel Event.
3. **End Events**:
        * Represent the termination point of a process or a specific activity within it.
        * There are six types of end events: Message End Event, Timer End Event, Conditional End Event (also known as Exclusive Choice), Multiple Instance End Event, Error End Event, and Compensation End Event.

Some key concepts to keep in mind when working with Events in BPMN:

* **Event-based processes**: These are processes that rely on specific events to trigger their execution.
* **Synchronization points**: Events can be used as synchronization points within a process flow, allowing for the coordination of multiple tasks or activities.
* **Flexibility and adaptability**: By incorporating events into a BPMN model, you can create more flexible and adaptable processes that respond to changing circumstances.

By using events effectively in your BPMN models, you can build processes that are not only efficient but also responsive to real-world scenarios.

Extract the events with it's types in this process description:
```
{process_description}
```
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
as a json expert represent the given events in a json list.

**Expected output**:
a valid json list object of this formate 
{
    "name":"string",
    "type":"string",
    "description":"string",
}

**The tasks**
{events}

**Notes**:
write the json inside a section of this formate

```json
the json object
```

"""
llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))

complete_prompt = PROMPT.replace("{events}", generate)

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