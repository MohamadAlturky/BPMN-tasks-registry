import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama

load_dotenv(override=True)

llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))

process_description = "Consider a process for purchasing items from an online shop. The user starts an order by logging in to their account. Then, the user simultaneously selects the items to purchase and sets a payment method. Afterward, the user either pays or completes an installment agreement. Since the reward value depends on the purchase value, After selecting the items, the user chooses between multiple options for a free reward. this step is done after selecting the items, but it is independent of the payment activities. Finally, the items are delivered. The user has the right to return items for exchange. Every time items are returned, a new delivery is made."

PROMPT="""
In Business Process Model and Notation (BPMN), **pools** and **lanes** are used to organize and structure a process diagram, helping to clarify responsibilities and interactions between different participants or departments.
- **Pools** are used to distinguish between different participants or entities in a process, often representing organizations or departments.
- **Lanes** within a pool are used to further detail roles, departments, or functions within the same organization or participant, clarifying who performs which tasks in the process.


Extract the pools and lanes in this process description:
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
as a json expert represent the given pools and lanes in a json list.

**Expected output**:
a valid json list object of this formate 
{
    "name":"string",
    "description":"string",
    "lanes":[
		{
			"name":"string",
   			"description":"string",
		}
	]
}

**The pools and lanes**
{pools_lanes}

**Notes**:
write the json inside a section of this formate

```json
the json object
```

"""
llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))

complete_prompt = PROMPT.replace("{pools_lanes}", generate)

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