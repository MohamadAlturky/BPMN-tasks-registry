import os
from pydantic import BaseModel
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

load_dotenv(override=True)

llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))

process_description = "Consider a process for purchasing items from an online shop. The user starts an order by logging in to their account. Then, the user simultaneously selects the items to purchase and sets a payment method. Afterward, the user either pays or completes an installment agreement. Since the reward value depends on the purchase value, After selecting the items, the user chooses between multiple options for a free reward. this step is done after selecting the items, but it is independent of the payment activities. Finally, the items are delivered. The user has the right to return items for exchange. Every time items are returned, a new delivery is made."

PROMPT = """
this is the extracted activities: {activities} \n from the process description: {process_description}.

You are a business process analyst expert help me to identify the sequence flow of the activities in the process which specified above. 

the structure of the output is a list of this format:
`

[From One activity] then [if there is a condition to proceed to the next step put it here otherwise put no condition] [To One activity] 

`
Notes:
- output the structured data and don't specify any thing else.
"""

activities = """
Process Return,
Return Items,
Deliver Items,
Complete Installment Agreement,
Pay,
Purchase,
Set Payment Method,
Choose Reward,
Select Items,
Login
"""
PROMPT = PROMPT.replace("{process_description}", process_description)
complete_prompt = PROMPT.replace("{activities}", activities)

# complete_prompt = """
# write a prompt to generate the flows between activities gatways and  in bpmn 
# """
generate = llm.invoke(complete_prompt)

print(generate)


PROMPT = """
extract bpmn in json from this structured sequence flow
{flow}

the desired output is a list of edges 
edge formate
{
    "from":"",
    "to":"",
    "condition":"",
}

notes: 
the from is the activity name
the to is the activity name
the condition is the condition to go from the first activity to the second one.
"""

complete_prompt = PROMPT.replace("{flow}", generate)


print()
print()
print()
print()
print()
generate = llm.invoke(complete_prompt)
print(generate)


print()
print()
print()
print()
print()
PROMPT = """
Extract all Gateway elements (Exclusive, Inclusive, Parallel) from the provided Business Process description. A Gateway is an element that controls the flow of activities in the process.

For each Gateway found, please answer the following questions:

Gateway Type: What type of Gateway is it? (Exclusive, Inclusive, Parallel)

Condition: What condition(s) determine which path to take?

Path Options: List all possible paths that can be taken after the Gateway.

Edge Triggers: Describe how the edge triggers are evaluated (e.g., based on user input, system data, or a specific event).

Successor Activities: Identify the activities that follow each path option.


Please provide your answers in a clear and concise format, highlighting the relevant sections of the original Business Process description where applicable.
this is the process description {text}
write the output as csv
"""
complete_prompt = PROMPT.replace("{text}", generate)

generate = llm.invoke(complete_prompt)
print(generate)
