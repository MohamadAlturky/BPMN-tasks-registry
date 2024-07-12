import os
from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
load_dotenv(override=True)

llm = Ollama(model="llama3", base_url=os.getenv("OLLAMA_HOST"))



agent = Agent(
        role="buissness process analyst",
        goal="rewrite the process description {process_description} in seperate paragraphs, each paragraph describes a complete process from start to end.",
        backstory="You work at a company to analyse processes and create a better understanding of the {process_idea} project.",
        allow_delegation=False,
        verbose=True, 
        llm = llm
    )
task = Task(
    description=(
        "the {process_description} describes the flow of the activities "
        "in the case of {process_idea}."
		"Make sure to use everything you know "
        "to rewrite the process into seperate complete paragraphs, "
        "please accuratly specify the seperate paragraphs and don't miss any activity."
    ),
    expected_output=(
	    "A detailed flows with a clear process flow."
    ),
    agent=agent,
)

executor =Crew(
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
result = executor.kickoff(inputs)
print(result)