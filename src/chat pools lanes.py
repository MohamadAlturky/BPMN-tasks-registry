import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama

load_dotenv(override=True)

llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))

process_description = "Consider a process for purchasing items from an online shop. The user starts an order by logging in to their account. Then, the user simultaneously selects the items to purchase and sets a payment method. Afterward, the user either pays or completes an installment agreement. Since the reward value depends on the purchase value, After selecting the items, the user chooses between multiple options for a free reward. this step is done after selecting the items, but it is independent of the payment activities. Finally, the items are delivered. The user has the right to return items for exchange. Every time items are returned, a new delivery is made."

PROMPT="""
In BPMN (Business Process Model and Notation), **Pools** and **Lanes** are used to represent a hierarchical organization of processes.

A **Pool** represents a high-level container that groups related processes together. It's essentially a swimlane for multiple processes, similar to how you might group related tasks in a Kanban board or workflow diagram. A pool typically corresponds 
to a single business entity, such as a company, department, or functional unit.

A **Lane**, on the other hand, represents a subdivision within a pool. Lanes are used to further break down the processes within a pool into smaller, more manageable groups. Think of lanes as subcategories or sub-processes that make up the overall process represented by the pool. Lanes can represent different teams, roles, or functional areas responsible for specific tasks within the pool.

Here's an example to illustrate this:

Suppose we have a company (pool) with two main departments: Sales and Marketing. Within these departments, there are several 
processes that need to be coordinated. We could represent this as follows:

* **Pool**: Company XYZ
        + **Lane**: Sales Team (within the pool)
                - Process 1: Lead Qualification
                - Process 2: Lead Conversion
        + **Lane**: Marketing Department (within the pool)
                - Process 3: Campaign Management
                - Process 4: Event Planning

In this example, the company is the pool, and within it, we have two lanes representing the Sales Team and Marketing Department. Each lane contains specific processes that are part of the overall business operation.
Extract the pools and lanes in this process description:
```
{process_description}
```


"""
llm = Ollama(model="llama3.1", base_url=os.getenv("OLLAMA_HOST"))

complete_prompt = PROMPT.replace("{process_description}", process_description)

generate = llm.invoke(complete_prompt)

print(generate)
print()
print()
print()
print()