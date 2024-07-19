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

PROMPT="""
As BPMN expert given the following process description:
{process_description}

and the activities in this process are:
{activities}

Return the model in the following format: activity nodes as words, parallel gateways as AND, exclusive 
gateways as XOR, and arcs as ->. You should number the gateways. You may also label the outgoing arcs of 
an exclusive gateway to denote the decision criterion, like XOR Gateway -> (condition 1) Task. 
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
PROMPT = PROMPT.replace("{process_description}", process_description)
complete_prompt = PROMPT.replace("{activities}", activities)

generate = llm.invoke(complete_prompt)

print(generate)

# class Activity(BaseModel):
#     name: str
#     type: str
#     description: str

# class Lane(BaseModel):
#     name: str
#     activities: list[Activity]

# class Pool(BaseModel):
#     name: str
#     lanes: list[Lane]

# class BPMN(BaseModel):
#     pools: list[Pool]



# agent = Agent(
#     role="python expert",
#     goal="Extract components from the given process description :'{text}'.",
#     backstory="",
#     allow_delegation=False,
#     verbose=True,
#     llm=llm
# )

# task = Task(
#     description=(
#         "Extract components from the given process description :'{text}'. "
#         """
#         the process description has this format
#         ```
#         Pool: [Pool Name]
#             Lane: [Lane Name]
#                 Activity: Name: [Activity Name], Type: [Activity Type], Description: [Activity Description].
#         ```
#         """
#     ),
#     expected_output=(
#         "A BPMN object containing a structured list of all BPMN components, including pools, lanes and activities."
#     ),
#     output_pydantic=BPMN,
#     agent=agent,
# )

# executor = Crew(
#     agents=[agent],
#     tasks=[task],
#     verbose=2
# )


# inputs = {
#     "text":generate
# }
# result = executor.kickoff(inputs)
# print(result)
