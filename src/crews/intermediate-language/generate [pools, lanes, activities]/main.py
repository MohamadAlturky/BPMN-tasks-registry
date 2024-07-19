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


Please create a concise and accurate representation of the process, including all relevant information and represent it in this format:

Output format
```
Pool: [Pool Name]
    Lane: [Lane Name]
        Activity: Name: [Activity Name], Type: [Activity Type], Description: [Activity Description].
```

Example output:
`
Pool: Ecommerce
    Lane: Shipping Department
        Activity: Name: Send the sales, Type: Task, Description: Load sales items into the car and drive to the delivery location.
`

Specific Requirements:

* Please do not include any unnecessary or redundant information.
* Use clear and concise language in the activity names, types, and descriptions.
* Ensure that the generated BPMN components are accurate, complete, and easy to understand.

Evaluation Criteria:

* Accuracy and completeness of the generated BPMN components
* Clarity and readability of the activity names, types, and descriptions
* Adherence to standard BPMN notation and conventions

Additional Notes:
By following these guidelines, I hope to receive a high-quality output that accurately represents the process description in a clear and concise manner.
Don't specify any thing else the formated Output. 
"""
complete_prompt = PROMPT.replace("{process_description}", process_description)

generate = llm.invoke(complete_prompt)

print(generate)

class Activity(BaseModel):
    name: str
    type: str
    description: str

class Lane(BaseModel):
    name: str
    activities: list[Activity]

class Pool(BaseModel):
    name: str
    lanes: list[Lane]

class BPMN(BaseModel):
    pools: list[Pool]



agent = Agent(
    role="python expert",
    goal="Extract components from the given process description :'{text}'.",
    backstory="",
    allow_delegation=False,
    verbose=True,
    llm=llm
)

task = Task(
    description=(
        "Extract components from the given process description :'{text}'. "
        """
        the process description has this format
        ```
        Pool: [Pool Name]
            Lane: [Lane Name]
                Activity: Name: [Activity Name], Type: [Activity Type], Description: [Activity Description].
        ```
        """
    ),
    expected_output=(
        "A BPMN object containing a structured list of all BPMN components, including pools, lanes and activities."
    ),
    output_pydantic=BPMN,
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
result = executor.kickoff(inputs)
print(result)
