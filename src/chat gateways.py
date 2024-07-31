import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama

load_dotenv(override=True)

llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))

process_description = "Consider a process for purchasing items from an online shop. The user starts an order by logging in to their account. Then, the user simultaneously selects the items to purchase and sets a payment method. Afterward, the user either pays or completes an installment agreement. Since the reward value depends on the purchase value, After selecting the items, the user chooses between multiple options for a free reward. this step is done after selecting the items, but it is independent of the payment activities. Finally, the items are delivered. The user has the right to return items for exchange. Every time items are returned, a new delivery is made."

PROMPT="""
In BPMN (Business Process Model and Notation), Gateways are used to control the flow of a process. They are essentially decision points that determine which path 
a process should take based on certain conditions.

There are four main types of Gateways in BPMN:

1. **Exclusive Gateway**:
        * Also known as an XOR (X-OR) gateway.
        * Used to make a choice between two or more paths, where only one path is taken at a time.
        * The process flow will continue along the first path that meets the conditions set for the gateway.
2. **Inclusive Gateway**:
        * Also known as an OR (inclusive OR) gateway.
        * Used when multiple paths can be taken simultaneously, based on certain conditions.
        * All paths connected to the inclusive gateway are executed if any of the conditions are met.
3. **Parallel Gateway**:
        * Also known as a AND (AND) gateway.
        * Used to start or join two or more parallel activities.
        * The process flow will continue along both paths simultaneously, until all activities have completed.
4. **Event-Based Gateway**:
        * Not strictly a gateway in the classical sense, but rather an event that triggers the execution of one or more branches.
        * Can be used to control the flow of a process based on external events.


Extract the gateways in this process description:
```
{process_description}
```

Notes:
- name the gateways
- show the inputs and outputs of the gateway
"""
llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))

complete_prompt = PROMPT.replace("{process_description}", process_description)

generate = llm.invoke(complete_prompt)

print(generate)
print()
print()
print()
print()




# PROMPT="""
# extract flow between the components of this process description
# **Process Description**:
# {process_description}

# **Notes**:
# - each connection has a type [direct connection,parallel point,decision point]
# - the output is a list of conections has this json structure 
#     `
#         source:[name],
#         distination:[name],
#         condition:[condition to move from the source to the distination],
#         type:[type]
#     `
# """
# llm = Ollama(model="llama3", base_url=os.getenv("OLLAMA_HOST"))

# complete_prompt = PROMPT.replace("{process_description}", generate)
# complete_prompt = complete_prompt.replace("\n", " ")
# complete_prompt = complete_prompt.replace("-", "\n-")

# generate = llm.invoke(complete_prompt)

# print(generate)