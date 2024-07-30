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

PROMPT="""
As a Business Process Modeling and Notation (BPMN) expert Given a text description of a business process:
{process_description}.

Here are the key elements:

1. **Process**: The overall process or task that needs to be modeled.
2. **Activities**:
	* **Tasks**: A specific action, like a calculation or an email, that is part of the process.
	* **Gateways**: Decision points where the flow of the process changes (AND, XOR, OR).
3. **Flows**:
	* **Sequence Flow**: The order in which activities are executed.
	* **Message Flow**: The exchange of information between processes or external systems.
4. **Events**:
	* **Start Event**: Marks the beginning of the process.
	* **End Event**: Marks the completion of the process.
	* **Intermediate Event**: A point within the process where something happens, like a timer or an exception.
5. **Gateways** (as mentioned earlier):
	* **AND Gateway**: The flow continues if all conditions are met.
	* **XOR Gateway**: The flow continues based on one condition being true.
	* **OR Gateway**: The flow continues based on any of the conditions being true.
6. **Data Objects**:
	* **Variables**: Data that is used within the process, like a customer ID or an order total.
	* **Input/Output Parameters**: Data that is exchanged with external systems or users.

When extracting these components, consider the following best practices:

1. Identify the main process and its subprocesses (if any).
2. Break down complex tasks into smaller, manageable activities.
3. Use events to represent decision points, exceptions, and other important milestones.
4. Ensure that flows accurately reflect the order of activities within the process.
5. Document data objects and their relationships with the process.

"""
llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))

complete_prompt = PROMPT.replace("{process_description}", process_description)

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


# llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))
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





# # # //////////////////////
# # # //////////////////////

# def get_activities(bpmn: BPMN) -> list[Activity]:
#     activities = []

#     for pool in bpmn.pools:
#         for lane in pool.lanes:
#             activities.extend(lane.activities)

#     return activities
# # # //////////////////////
# # # //////////////////////

# activities = get_activities(result)
# print("Activities")
# print("Activities")
# print("Activities")

# activities_names = ""
# for activity in activities:
#     print(activity.name)
#     activities_names = activities_names +"\n"+ activity.name

# print("activities_names ")
# print("activities_names ")
# print("activities_names ")
# print("activities_names ")
# print(activities_names)

# # # //////////////////////
# # # //////////////////////

# llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))

# # process_description = "Consider a process for purchasing items from an online shop. The user starts an order by logging in to their account. Then, the user simultaneously selects the items to purchase and sets a payment method. Afterward, the user either pays or completes an installment agreement. Since the reward value depends on the purchase value, After selecting the items, the user chooses between multiple options for a free reward. this step is done after selecting the items, but it is independent of the payment activities. Finally, the items are delivered. The user has the right to return items for exchange. Every time items are returned, a new delivery is made."

# PROMPT = """
# this is the extracted activities: {activities} \n from the process description: {process_description}.

# You are a BPMN expert help me to identify the sequence flow of the activities and the gateways in the process which specified above. 

# the structure of the output is a list of this format:
# `
# [From One activity Or Gateway] then [if there is a condition to proceed to the next step put it here otherwise put no condition] [To One activity Or Gateway] 
# `
# Notes:
# - output the structured data and don't specify any thing else. 
# - the gateway name s the type of it plus a unique number.
# """

# # activities = """
# # Process Return,
# # Return Items,
# # Deliver Items,
# # Complete Installment Agreement,
# # Pay,
# # Purchase,
# # Set Payment Method,
# # Choose Reward,
# # Select Items,
# # Login
# # """
# PROMPT = PROMPT.replace("{process_description}", process_description)
# complete_prompt = PROMPT.replace("{activities}", activities_names)

# # # complete_prompt = """
# # # write a prompt to generate the flows between activities gatways and  in bpmn 
# # # """
# generate = llm.invoke(complete_prompt)

# print(generate)


# PROMPT = """
# extract bpmn in json from this structured sequence flow
# {flow}

# the desired output is a list of edges 
# edge formate
# {
#     "source":"",
#     "destination":"",
#     "condition":"",
# }

# notes: 
# the source is the activity name
# the destination is the activity name
# the condition is the condition to go from the first activity to the second one.
# """
# # # if there is a gateway put it in the from section or the to section the gateway name is the type of it and a unique number

# complete_prompt = PROMPT.replace("{flow}", generate)


# print()
# print()
# print()
# print()
# print()
# llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))
# generate = llm.invoke(complete_prompt)
# print(generate)


# print()
# print()
# print()
# print()

# class Connection(BaseModel):
#     source: str
#     destination: str
#     condition: str


# class Connections(BaseModel):
#     connections : list[Connection]
# llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))

# agent = Agent(
#     role="python expert",
#     goal="Extract components from the given sequence flow :'{text}'.",
#     backstory="",
#     allow_delegation=False,
#     verbose=True,
#     llm=llm
# )

# task = Task(
#     description=(
#         "Extract components from the given sequence flow :'{text}' that respresented in a json format."
#         """
#         the sequence flow is a list this format
#         ```
            
#             "source": Name
#             "destination": Name
#             "condition": description
            
#         ```
#         """
#     ),
#     expected_output=(
#         "A Connections object containing a structured list of connections each connection has the source ,destination and the condition to go from source to destination."
#     ),
#     output_pydantic=Connections,
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




# print("")
# print("")
# print("")
# print("")

# print("")
# print("")
# print("")
# print(result)