import os
from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from pydantic import BaseModel

class Content(BaseModel):
    content: str

class Paragraphs(BaseModel):
    paragraphs: list[Content]

load_dotenv(override=True)

llm = Ollama(model="llama3", base_url=os.getenv("OLLAMA_HOST"))

agent = Agent(
    role="business process analyst",
    goal="Rewrite the given process description '{process_description}' into separate paragraphs. Each paragraph should describe a complete process from start to end, clearly outlining each independent flow.",
    backstory="As a business process analyst at your company, your job is to analyze and improve the understanding of the '{process_idea}' project by breaking down its process descriptions into clear, standalone components.",
    allow_delegation=False,
    verbose=True,
    llm=llm
)

task = Task(
    description=(
        "The '{process_description}' outlines the sequence of activities for the '{process_idea}' project. "
        "Your task is to use your expertise to rewrite this description into separate, clear paragraphs. "
        "Each paragraph must detail a complete process flow from start to end, ensuring no activity is overlooked."
    ),
    expected_output=(
        "A set of detailed paragraphs, each representing an independent process flow with clear start-to-end steps."
    ),
    output_pydantic=Paragraphs,
    agent=agent,
)

executor = Crew(
    agents=[agent],
    tasks=[task],
    verbose=2
)

inputs = {
    "process_description": """
        Consider a process for purchasing items
        from an online shop. The user starts an order by logging in to their account.
        Then, the user simultaneously selects the items to purchase and sets a payment
        method. Afterward, the user either pays or completes an installment agreement.
        Since the reward value depends on the purchase value,
        After selecting the items, the user chooses between multiple options for a free reward.
        this step is done after selecting the items,
        but it is independent of the payment activities.
        Finally, the items are delivered. The user has the right to
        return items for exchange. Every time items are returned,
        a new delivery is made.
    """,
    "process_idea": "Ecommerce app",
}

result :Paragraphs = executor.kickoff(inputs)
print(result)

for i in result.paragraphs:
    print("Paragraph")
    print()
    print(i.content)
    print()