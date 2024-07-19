import os
from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from pydantic import BaseModel
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

PROMPT = """
I want you to create a Business Process Model and Notation (BPMN) model for the process described below. Return the model in the following format: task nodes as Task [words], subprocess nodes as Subprocess [words], call activity nodes as Call Activity [words], events as Event [Event Name], parallel gateways as AND, exclusive gateways as XOR, and arcs as ->. Pools and Swimlanes should be used to represent different actors or departments involved in the process.

    - Start Event: Represented as Start Event O.
    - End Event: Represented as Event End O.
    - Intermediate Events: Represented as Event [Event Name].
    - Task: Represented as Task [Task Name].
    - Subprocess: Represented as Subprocess [Subprocess Name].
    - Call Activity: Represented as Call Activity [Activity Name].
    - Exclusive Gateway: Represented as XOR Gateway #.
    - Parallel Gateway: Represented as AND Gateway #.
    - Pools and Swimlanes: Pools represent the overall participant (e.g., company, department), and Swimlanes within Pools represent different roles or actors.

    Use numbering for gateways for clarity. You may also label the outgoing arcs of an exclusive gateway to denote the decision criterion,
    like XOR Gateway 1 -> Condition (action choice).
    Additionally, provide a mapping of actors to activities in the format Actor: [activity1, ...]

    Here's an example for better understanding:

    Pool [Order Management] 
        Swimlane [Sales]
            Start Event O -> Task [Receive Order]
            Task [Receive Order] -> XOR Gateway 1
            XOR Gateway 1 -> Condition (Order Valid)
            XOR Gateway 1 -> Condition (Order Invalid)
            Condition (Order Valid) -> Task [Process Order]
            Condition (Order Invalid) -> Event End O

        Swimlane [Inventory]
            Task [Process Order] -> AND Gateway 1
            AND Gateway 1 -> Task [Check Stock]
            AND Gateway 1 -> Task [Update Inventory]
            Task [Check Stock] -> XOR Gateway 2
            XOR Gateway 2 -> Condition (Stock Available)
            XOR Gateway 2 -> Condition (Stock Not Available)
            Condition (Stock Available) -> Task [Reserve Stock]
            Condition (Stock Not Available) -> Task [Notify Sales]

        Swimlane [Shipping]
            Task [Reserve Stock] -> Task [Prepare Shipment]
            Task [Prepare Shipment] -> Task [Ship Order]
            Task [Ship Order] -> Event End O

    Actor Mapping:
    Sales: [Receive Order, Process Order]
    Inventory: [Check Stock, Update Inventory, Reserve Stock, Notify Sales]
    Shipping: [Prepare Shipment, Ship Order]

    Process description: {process_description}

    Let's work this out in a step-by-step way to ensure we have a well-defined workflow.
    Firstly, think logically for a well-defined workflow, 
    avoiding common modeling issues like deadlocks and unconnected broken flows.
"""

process_description = "Order processing starts when a customer places an order. The order is received by the sales department and checked for validity. If the order is valid, it is processed and sent to the inventory department to check stock. If the stock is available, it is reserved, and the order is sent to the shipping department to prepare and ship the order. If the stock is not available, the sales department is notified. The process ends when the order is shipped or if the order is invalid."

complete_prompt = PROMPT.replace("{process_description}", process_description)
generate = llm.invoke(complete_prompt)
print(bcolors.WARNING + "The Results Is Back!!!" + bcolors.ENDC)
print(bcolors.OKGREEN+generate+ bcolors.ENDC)



from pydantic import BaseModel, Field
from typing import List, Dict

class BPMNTask(BaseModel):
    description: str

class BPMNEvent(BaseModel):
    event_type: str
    name: str

class GatewayCondition(BaseModel):
    condition_content : str
    activity:str

class BPMNGateway(BaseModel):
    gateway_type: str
    number: int
    conditions: List[GatewayCondition]  # Condition description mapped to next activity description

    
class BPMNArc(BaseModel):
    source: str
    target: str
    condition: str = None  # Optional field for conditions on arcs

class BPMNSwimlane(BaseModel):
    name: str
    activities: List[str]

class BPMNPool(BaseModel):
    name: str
    swimlanes: List[BPMNSwimlane]

class BPMNActorMapping(BaseModel):
    actor: str
    activities: List[str]

class BPMNModel(BaseModel):
    pools: List[BPMNPool]
    events: List[BPMNEvent]
    tasks: List[BPMNTask]
    gateways: List[BPMNGateway]
    arcs: List[BPMNArc]
    actor_mapping: List[BPMNActorMapping]

###################################################################
###################################################################
# Define the agent with detailed instructions
agent = Agent(
    role="business process analyst",
    goal="Extract all BPMN components from the given process description :'{text}' and organize them for BPMN diagram generation.",
    backstory="As a business process analyst, you analyze process descriptions to extract and organize elements needed for creating BPMN diagrams.",
    allow_delegation=False,
    verbose=True,
    llm=llm
)

# Define the task with detailed instructions
task = Task(
    description=(
        "Extract all BPMN components from the given process description :'{text}'. "
    ),
    expected_output=(
        "A BPMNModel object containing a structured list of all BPMN components, including pools, swimlanes, tasks, subprocesses, call activities, events, gateways, arcs, and actor mappings, formatted for BPMN diagram creation."
    ),
    output_pydantic=BPMNModel,
    agent=agent,
)

# Execute the task
executor = Crew(
    agents=[agent],
    tasks=[task],
    verbose=2
)



inputs = {
    "text":generate
}

result = executor.kickoff(inputs)
print(result)


# # Example of instantiating a BPMNModel
# example_bpmn_model = BPMNModel(
#     pools=[
#         BPMNPool(
#             name="Order Processing",
#             swimlanes=[
#                 BPMNSwimlane(name="Sales", activities=["Receive Order", "Process Order"]),
#                 BPMNSwimlane(name="Inventory", activities=["Check Stock", "Update Inventory", "Reserve Stock", "Notify Sales"]),
#                 BPMNSwimlane(name="Shipping", activities=["Prepare Shipment", "Ship Order"]),
#             ]
#         )
#     ],
#     events=[
#         BPMNEvent(event_type="Start Event", name="O"),
#         BPMNEvent(event_type="End Event", name="O"),
#     ],
#     tasks=[
#         BPMNTask(description="Receive Order"),
#         BPMNTask(description="Process Order"),
#         BPMNTask(description="Check Stock"),
#         BPMNTask(description="Update Inventory"),
#         BPMNTask(description="Reserve Stock"),
#         BPMNTask(description="Notify Sales"),
#         BPMNTask(description="Prepare Shipment"),
#         BPMNTask(description="Ship Order"),
#     ],
#     gateways=[
#         BPMNGateway(
#             gateway_type="XOR",
#             number=1,
#             conditions={"Order Valid": "Process Order", "Order Invalid": "End Event O"}
#         ),
#         BPMNGateway(
#             gateway_type="AND",
#             number=1,
#             conditions={"Check Stock": "XOR Gateway 2", "Update Inventory": "Check Stock"}
#         ),
#         BPMNGateway(
#             gateway_type="XOR",
#             number=2,
#             conditions={"Stock Available": "Reserve Stock", "Stock Not Available": "Notify Sales"}
#         )
#     ],
#     arcs=[
#         BPMNArc(source="Start Event O", target="Receive Order"),
#         BPMNArc(source="Receive Order", target="XOR Gateway 1"),
#         BPMNArc(source="XOR Gateway 1", target="Process Order", condition="Order Valid"),
#         BPMNArc(source="XOR Gateway 1", target="End Event O", condition="Order Invalid"),
#         BPMNArc(source="Process Order", target="AND Gateway 1"),
#         BPMNArc(source="AND Gateway 1", target="Check Stock"),
#         BPMNArc(source="AND Gateway 1", target="Update Inventory"),
#         BPMNArc(source="Check Stock", target="XOR Gateway 2"),
#         BPMNArc(source="XOR Gateway 2", target="Reserve Stock", condition="Stock Available"),
#         BPMNArc(source="XOR Gateway 2", target="Notify Sales", condition="Stock Not Available"),
#         BPMNArc(source="Reserve Stock", target="Prepare Shipment"),
#         BPMNArc(source="Prepare Shipment", target="Ship Order"),
#         BPMNArc(source="Ship Order", target="End Event O"),
#     ],
#     actor_mapping=[
#         BPMNActorMapping(actor="Sales", activities=["Receive Order", "Process Order"]),
#         BPMNActorMapping(actor="Inventory", activities=["Check Stock", "Update Inventory", "Reserve Stock", "Notify Sales"]),
#         BPMNActorMapping(actor="Shipping", activities=["Prepare Shipment", "Ship Order"]),
#     ]
# )
