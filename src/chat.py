import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama

load_dotenv(override=True)

llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))

process_description = "Consider a process for purchasing items from an online shop. The user starts an order by logging in to their account. Then, the user simultaneously selects the items to purchase and sets a payment method. Afterward, the user either pays or completes an installment agreement. Since the reward value depends on the purchase value, After selecting the items, the user chooses between multiple options for a free reward. this step is done after selecting the items, but it is independent of the payment activities. Finally, the items are delivered. The user has the right to return items for exchange. Every time items are returned, a new delivery is made."

PROMPT="""
rewrite this process description to clarify the sequence flow, decision points, the parallel paths of the process
```
{process_description}
```
Notes:
- annotate each activity with number 
- the parallel paths are the points where the flow goes to the next activities with no condition  
- the decision points are the points where the flow goes to the next activities with some condition for each one  
- The parallel paths should be marked with (parallel path) and the decision points are annotated with "Decision Point [number]".

"""
llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))

complete_prompt = PROMPT.replace("{process_description}", process_description)

generate = llm.invoke(complete_prompt)

print(generate)
print()
print()
print()
print()




PROMPT="""
extract flow between the components of this process description
**Process Description**:
{process_description}

**Notes**:
- each connection has a type [direct connection,parallel point,decision point]
- the output is a list of conections has this json structure 
    `
        source:[name],
        distination:[name],
        condition:[condition to move from the source to the distination],
        type:[type]
    `
"""
llm = Ollama(model="llama3", base_url=os.getenv("OLLAMA_HOST"))

complete_prompt = PROMPT.replace("{process_description}", generate)
complete_prompt = complete_prompt.replace("\n", " ")
complete_prompt = complete_prompt.replace("-", "\n-")

generate = llm.invoke(complete_prompt)

print(generate)