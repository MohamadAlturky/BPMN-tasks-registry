import os
from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from pydantic import BaseModel

class Swimlane(BaseModel):
    name : str

class Pool(BaseModel):
    name: str
    swimlanes: list[Swimlane]

class PoolsAndSwimlanes(BaseModel):
    pools: list[Pool]

load_dotenv(override=True)

llm = Ollama(model="llama3", base_url=os.getenv("OLLAMA_HOST"))

agent = Agent(
    role="business process analyst",
    goal="Extract pools and swimlanes from the given process description and organize them for BPMN diagram generation.",
    backstory="As a business process analyst, you analyze process descriptions to extract and organize elements needed for creating BPMN diagrams.",
    allow_delegation=False,
    verbose=True,
    llm=llm
)

task = Task(
    description=(
        "Extract the pools and swimlanes from the given process description. "
        "Each pool should represent a major participant (e.g., organization or system), "
        "and each swimlane should represent specific roles or departments within these pools. "
        "List each pool and its corresponding swimlanes, and for each swimlane, provide a sequence of activities. "
        "Ensure each activity is clearly associated with its respective pool and swimlane."
    ),
    expected_output=(
        "A structured list of pools and swimlanes with their respective activities, formatted for BPMN diagram creation."
    ),
    output_pydantic=PoolsAndSwimlanes,
    agent=agent,
)

executor = Crew(
    agents=[agent],
    tasks=[task],
    verbose=2
)

inputs = {
    "process_description": """
        Consider a process for purchasing items from an online shop. The user starts an order by logging in to their account.
        Then, the user simultaneously selects the items to purchase and sets a payment method. Afterward, the user either pays or completes an installment agreement.
        Since the reward value depends on the purchase value, after selecting the items, the user chooses between multiple options for a free reward.
        This step is done after selecting the items, but it is independent of the payment activities.
        Finally, the items are delivered. The user has the right to return items for exchange. Every time items are returned, a new delivery is made.
    """
}

result : PoolsAndSwimlanes = executor.kickoff(inputs)
print(result)


for i in result.pools:
    print("pool")
    print(i.name)
    print("swimlanes")
    for j in i.swimlanes:
        print(j.name)
    print()
