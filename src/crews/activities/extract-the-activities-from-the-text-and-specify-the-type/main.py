import os
from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from pydantic import BaseModel

class Activity(BaseModel):
    name: str
    type: str
    sequence: int

class Activities(BaseModel):
    activities: list[Activity]

load_dotenv(override=True)

llm = Ollama(model="llama3", base_url=os.getenv("OLLAMA_HOST"))

agent = Agent(
    role="business process analyst",
    goal="Extract activities from the given process description {process_description}, specify their types, and organize them for BPMN diagram generation.",
    backstory="As a business process analyst, you analyze process descriptions to extract and organize activities with their types needed for creating BPMN diagrams.",
    allow_delegation=False,
    verbose=True,
    llm=llm
)

task = Task(
    description=(
        "Extract the activities from the given process description {process_description}. "
        "Each activity should represent a distinct step in the process, with a clear type indicating whether it is a user task, service task, etc. "
        "List each activity in the order it occurs, ensuring each activity is clearly described, typed, and sequenced appropriately."
    ),
    expected_output=(
        "A structured list of activities with their respective types and sequences, formatted for BPMN diagram creation."
    ),
    output_pydantic=Activities,
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

result: Activities = executor.kickoff(inputs)
