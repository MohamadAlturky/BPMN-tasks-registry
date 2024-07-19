import os
from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from pydantic import BaseModel

class NodeData(BaseModel):
    label : str
    component_type : str


class NodeStyle(BaseModel):
    width : str
    height : str
    backgroundColor: str
    borderRadius : str


class NodePosition(BaseModel):
    x : int
    y : int

class Node(BaseModel):
    id: str
    data: NodeData
    style: NodeStyle
    position: NodePosition
    className: str
    type: str
    focusable: bool
    parentId: str
    extent: str
    draggable: bool


# load_dotenv(override=True)

# llm = Ollama(model="llama3", base_url=os.getenv("OLLAMA_HOST"))

# agent = Agent(
#     role="business process analyst",
#     goal="Extract BPMN events from the given process description '{process_description}' and organize them for BPMN diagram generation.",
#     backstory="As a business process analyst, you analyze process descriptions to extract and organize BPMN events.",
#     allow_delegation=False,
#     verbose=True,
#     llm=llm
# )

# task = Task(
#     description=(
#         "Extract the BPMN events from the given process description '{process_description}'. "
#         "Categorize each event as a Start Event, Intermediate Event, or End Event. "
#         "Provide a brief description for each event, and ensure they are clearly associated with their respective type."
#     ),
#     expected_output=(
#         "A structured list of BPMN events categorized into Start Events, Intermediate Events, and End Events, formatted for BPMN diagram creation."
#     ),
#     output_pydantic=BPMNEvents,
#     agent=agent,
# )

# executor = Crew(
#     agents=[agent],
#     tasks=[task],
#     verbose=2
# )

# inputs = {
#     "process_description": """
#         Consider a process for purchasing items from an online shop. The user starts an order by logging in to their account.
#         Then, the user simultaneously selects the items to purchase and sets a payment method. Afterward, the user either pays or completes an installment agreement.
#         Since the reward value depends on the purchase value, after selecting the items, the user chooses between multiple options for a free reward.
#         This step is done after selecting the items, but it is independent of the payment activities.
#         Finally, the items are delivered. The user has the right to return items for exchange. Every time items are returned, a new delivery is made.
#     """
# }

# result: BPMNEvents = executor.kickoff(inputs)

# print(result)

# print()
# print("intermediate_events")
# for i in result.intermediate_events:
#     print(i.name)
#     print(i.description)
    
    
# print()
# print("start_events")
# for i in result.start_events:
#     print(i.name)
#     print(i.description)
    
    
    

# print()
# print("end_events")
# for i in result.end_events:
#     print(i.name)
#     print(i.description)