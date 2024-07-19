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

llm = Ollama(model="llama3", base_url=os.getenv("OLLAMA_HOST"))

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
