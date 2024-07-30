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
Here are the step-by-step instructions to extract activities, gateways (decision and merge), and relationships between them from a process description to generate BPMN diagrams:

**Step 1: Understand the Process Description**

Read the process description carefully to understand what is being described. This may be in the form of text, flowcharts, or other visual representations.

**Step 2: Identify Activities (Tasks)**

Identify and extract all tasks or activities that are performed within the process. These are typically represented by verbs, such as:

* Receive
* Process
* Validate
* Calculate
* Send
* Meet
* Call
* Review
* etc.

Note down each activity in a list.

**Step 3: Identify Gateways (Decisions and Merges)**

Identify and extract all decision points or merge points within the process. These are typically represented by words or phrases that indicate a choice or a joining of paths, such as:

* If
* Then
* Else
* Or
* And
* When
* Where
* etc.

Also, identify any activities that have multiple outcomes or paths, which may be represented by merge gateways.

Note down each gateway in a separate list.

**Step 4: Determine Relationships between Activities and Gateways**

Determine the relationships between activities and gateways based on the process description. These relationships may include:

* **Sequence**: One activity follows another.
* **Parallel**: Two or more activities are performed simultaneously.
* **Choice**: A decision point (gateway) leads to multiple possible paths.
* **Merge**: Multiple paths converge at a merge point (gateway).
* **Loop**: An activity is repeated while a condition is met.

Note down each relationship in a separate list, using the following notation:

Activity A → Activity B (sequence)
Activity C || Activity D (parallel)
Gateway E → Activity F (choice)
Activity G ⇐ Gateway H (merge)
Activity I → Gateway J (loop)

**Step 5: Review and Refine**

Review your lists of activities, gateways, and relationships to ensure that they accurately reflect the process description. Refine any inconsistencies or ambiguities.

With these instructions, you should be able to extract the necessary information from a process description to generate BPMN diagrams.
"""
llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))

complete_prompt = PROMPT.replace("{process_description}", process_description)

generate = llm.invoke(complete_prompt)

print(generate)

