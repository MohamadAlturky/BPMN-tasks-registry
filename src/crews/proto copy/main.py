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
As a BPMN expert Given a text description of a business process:
{process_description}.

identify and extract the following essential components to create a comprehensive Business Process Modeling and Notation (BPMN) diagram:

1. **Process Name**: Identify the name of the business process being described.
2. **Scope and Context**: Determine the scope and context of the process, including any relevant organizational units, departments, or external parties involved.
3. **Primary Actor(s)**: Identify the primary actor(s) responsible for initiating and executing the process (e.g., customers, employees, managers).
4. **Data Input/Output**: Determine the types of data input/output for each task or activity, such as forms, reports, or external systems interactions.

By carefully extracting and analyzing these essential components from a text description, you can create a comprehensive BPMN diagram that accurately represents the business process in question.
"""
llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))

complete_prompt = PROMPT.replace("{process_description}", process_description)

generate = llm.invoke(complete_prompt)

print()
print()
print()
print(generate)
print()
print()
print()

######### 
######### 
######### 
######### 
######### 
######### 
######### 
######### 

llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))

process_description = "Consider a process for purchasing items from an online shop. The user starts an order by logging in to their account. Then, the user simultaneously selects the items to purchase and sets a payment method. Afterward, the user either pays or completes an installment agreement. Since the reward value depends on the purchase value, After selecting the items, the user chooses between multiple options for a free reward. this step is done after selecting the items, but it is independent of the payment activities. Finally, the items are delivered. The user has the right to return items for exchange. Every time items are returned, a new delivery is made."

PROMPT="""
As a BPMN expert Given a text description of a business process:
{process_description}.

identify and extract the following essential components to create a comprehensive Business Process Modeling and Notation (BPMN) diagram:

1. **Trigger Events**: Extract any trigger events that initiate the process, such as user requests, system notifications, or external stimuli.
2. **Process Flow**: Break down the text description into individual steps or tasks to create a high-level process flow diagram.
3. **Gateways and Decisions**: Identify decision points, gateways (AND, OR, XOR), and conditional logic within the process flow.
4. **Tasks and Activities**: Extract specific tasks and activities involved in each step of the process, including any necessary inputs, outputs, or resources required.
5. **Error Handling and Recovery**: Identify potential errors, exceptions, or exceptions handling mechanisms within the process flow.
6. **Synchronization Points**: Extract any synchronization points where multiple tasks or activities need to be coordinated.

By carefully extracting and analyzing these essential components from a text description, you can create a comprehensive BPMN diagram that accurately represents the business process in question.
"""
llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))

complete_prompt = PROMPT.replace("{process_description}", process_description)

generate = llm.invoke(complete_prompt)
print()
print()
print()
print(generate)
print()
print()
print()


######### 
######### 
######### 
######### 
######### 
######### 
######### 
######### 

llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))

process_description = "Consider a process for purchasing items from an online shop. The user starts an order by logging in to their account. Then, the user simultaneously selects the items to purchase and sets a payment method. Afterward, the user either pays or completes an installment agreement. Since the reward value depends on the purchase value, After selecting the items, the user chooses between multiple options for a free reward. this step is done after selecting the items, but it is independent of the payment activities. Finally, the items are delivered. The user has the right to return items for exchange. Every time items are returned, a new delivery is made."

PROMPT="""
You are a business process modeling expert given this extracted elements.
{elements}.

identify and extract the the sequence flow between activities and gateways to create a comprehensive Business Process Modeling and Notation (BPMN) diagram.
By carefully extracting and analyzing these sequence flow between activities and gateways for creating a comprehensive BPMN diagram.
the desired output is a list of this formate:
`
    [source] the [condition] to [distination]
` 
"""
llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))

complete_prompt = PROMPT.replace("{elements}", generate)

generate = llm.invoke(complete_prompt)
print()
print()
print()
print(generate)
print()
print()
print()


######### 
######### 
######### 
######### 
######### 
######### 
######### 
######### 


PROMPT = """
extract bpmn in json from this structured sequence flow
{flow}

the desired output is a list of edges 
edge formate
{
    "source":"",
    "destination":"",
    "condition":"",
}

notes: 
the source is the activity name
the destination is the activity name
the condition is the condition to go from the first activity to the second one.
"""
# # if there is a gateway put it in the from section or the to section the gateway name is the type of it and a unique number

complete_prompt = PROMPT.replace("{flow}", generate)


print()
print()
print()
print()
print()
llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))
generate = llm.invoke(complete_prompt)
print(generate)




##############
############
############
############
############
############
############


print()
print()
print()
print()

class Connection(BaseModel):
    source: str
    destination: str
    condition: str


class Connections(BaseModel):
    connections : list[Connection]
llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))

agent = Agent(
    role="python expert",
    goal="Extract components from the given sequence flow :'{text}'.",
    backstory="",
    allow_delegation=False,
    verbose=True,
    llm=llm
)

task = Task(
    description=(
        "Extract components from the given sequence flow :'{text}' that respresented in a json format."
        """
        the sequence flow is a list this format
        ```
            
            "source": Name
            "destination": Name
            "condition": description
            
        ```
        """
    ),
    expected_output=(
        "A Connections object containing a structured list of connections each connection has the source ,destination and the condition to go from source to destination."
    ),
    output_pydantic=Connections,
    agent=agent,
)

executor = Crew(
    agents=[agent],
    tasks=[task],
    verbose=2
)


inputs = {
    "text":generate
}
result :Connections= executor.kickoff(inputs)




print("")
print("")
print("")
print("")

print("")
print("")
print("")
print(result)
for i in result.connections:
    print("source : ",i.source)
    print("destination : ",i.destination)
    print("condition : ",i.condition)
    
    
from typing import List, Dict

def connections_to_graph(connections: List[Connection]) -> Dict:
    """
    Converts a list of Connection objects to a graph data structure.

    Args:
        connections (List[Connection]): A list of Connection objects.

    Returns:
        Dict: A dictionary with node and edge information.
    """

    # Initialize an empty graph
    graph = {
        "nodes": set(),
        "edges": {}
    }

    # Iterate over each connection in the list
    for conn in connections:
        # Add source and destination to nodes if not already present
        graph["nodes"].add(conn.source)
        graph["nodes"].add(conn.destination)

        # Create an edge between source and destination if not already present
        if conn.source not in graph["edges"]:
            graph["edges"][conn.source] = set()
        if conn.destination not in graph["edges"]:
            graph["edges"][conn.destination] = set()

        # Add the connection to the edges dictionary
        graph["edges"][conn.source].add(conn.destination)
        graph["edges"][conn.destination].add(conn.source)

    return graph



graph_data = connections_to_graph(result.connections)
print(graph_data)  