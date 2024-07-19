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
I want you to create a Business Process Model and Notation (BPMN) model for the process described 
below. Return the model in the following format: task nodes as words, parallel gateways as AND, exclusive 
gateways as XOR, and arcs as ->. You should number the gateways. You may also label the outgoing arcs of 
an exclusive gateway to denote the decision criterion, like XOR Gateway -> (condition 1) Task.

Process description:
{process_description}
"""

activities = """
Process Return,
Return Items,
Deliver Items,
Complete Installment Agreement,
Pay,
Set Payment Method,
Choose Reward,
Login
"""
complete_prompt = PROMPT.replace("{process_description}", process_description)
# complete_prompt = PROMPT.replace("{activities}", activities)

# complete_prompt = """
# write a prompt to generate the flows between activities gatways and  in bpmn 
# """
generate = llm.invoke(complete_prompt)

print(generate)
