Your role: you are an expert in process modeling, familiar with common process constructs such as exclusive choice, do-redo loops, and partial orders. Your task is to analyze the textual description of a process and transform it into a process model in the POWL language. When generating a model, be as precise as possible and capture all details of the process in the model. Also act as the process owner and use your expertise and familiarity with the process context to fill in any missing knowledge.

Use the following knowledge about the POWL process modeling language:
A POWL model is a hierarchical model. POWL models are recursively generated by combining submodels into a new model either using an operator (xor or loop) or as a partial order.  We define three types of POWL models. The first type of POWL models is the base case consisting of a single activity. For the second type of POWL models, we use an operator (xor or loop) to combine multiple POWL models into a new model. We use xor to model an exclusive choice of n >= 2 sub-models. We use the operator loop to model a do-redo loop of 2 POWL models. The third type of POWL models is defined as a partial order over n >= 2 submodels. A partial order is binary relation that is irreflexive, transitive, and asymmetry.

Provide the Python code that recursively generate a POWL model. Save the final model is the variable 'final_model'. Do not try to execute the code, just return it. Assume the class ModelGenerator is properly implemented and can be imported using the import statement: from utils.model_generation import ModelGenerator. ModelGenerator provides the functions described below:
 - activity(label) generates an activity. It takes 1 string arguments, which is the label of the activity.
 - xor(*args) takes n >= 2 arguments, which are the submodels. Use it to model an exclusive choice structures, i.e., if you have several possible paths where only one of them can be taken (either or), thenyou use xor to combine them. If a decision is made based on some condition at some point in a process, you should model an exclusive choice between the two paths starting after this decision xor(path_1 path_2) where path_1 and path_2 are subprocess that encapsulates the full sequence of actions following each decision. You can use xor(submodel, None) to make a submodel optional; i.e., to model anexclusive choice between executing this submodel or skipping it.
 - loop(do, redo) takes 2 arguments, which are the do and redo parts. Use it to model cyclic behavior; i.e., the do part is executed once first, and every time the redo part is executed, it is followed by another execution of the do part. You can also use loop to model a self-loop by setting the redo part to None; i.e., to indicate that the do part can be repeated from 1 to as many times as possible. You can also model a skippable self-loop by setting the do part to None instead; i.e., to indicate that the redo part can be repeated from 0 to as many times as possible. You can use a self-loop to model that in a complicated process you can go back to certain initial stage: first you model the complicated process, then you put it inside a loop.
 - partial_order(dependencies) takes 1 argument, which is a list of tuples of submodels. These tuples set the nodes of the partial order and specify the edges of the partial order (i.e., the sequential dependencies). The transitive closure of the added dependencies should conform with the irreflexivity requirement of partial orders. We interpret unconnected nodes in a partial order to be concurrent and connections between nodes as sequential dependencies. Use a partial order with no edges (with the parameter 'dependencies' set to a list of tuples of size 1) to model pure concurrency/independency; i.e., to model the relation  between sub models that can all be happens at the same time/in any order. However, note that all of them need to happen unlike the xor case. The main difference is that with xor case you model alternative paths (either path_1 or path_2), while with a partial order you model concurrent paths (you do both path_1 and path_2). The general assumption is partial orders is that nodes are concurrent; however, you can still add sequential dependencies between certain nodes (as tuples in the list for the parameter 'dependencies'). For example, this is the case in systems where you execute all subprocesses but one of them must be completed before starting another one. Assume we have 4 submodel A, B, C, D. partial_order(dependencies=[(A, B), (B, C), (C, D)]) models a sequence A -> B -> C -> D; partial_order(dependencies=[(A,), (B,), (C,), (D,)]) models full concurrency; partial_order(dependencies=[(A,B), (C,), (D,)]) models concurrency with the sequential dependency A -> B. Avoid using a partial order as a child of another partial order to ensure not leaving out any sequential dependencies. To resolve this, you can combine the two orders.
Note: for any powl model, you can always call powl.copy() to create another instance of the same model. This is useful to model cases where a subporcess or activity can be executed exactlytwice (not really in a loop).

Avoid common mistakes. First, ensure that the transitive closure of the generated partial orders do not violate irreflexivity. Verify that all optional/skippable and repeatable parts are modeled correctly. Also validate that the same submodel is not used multiple times (e.g., in xor then in partial_oder)! You have three ways for avoiding this depending on the case: (1) consider using loops to model cyclic behaviour; (2) if you instead want to create a second instance of the same submodel, consider creating a copy of it; (3) if none of these two cases apply, then your structure is not correct. Ensure that you correctly model xor/loop between larger complete alternative/loop paths (i.e., between full paths, not decision points). Finally, do not create partial orders as children of other partial orders.  Instead, combine dependencies at the same hierarchical level to avoid nested partial orders. Example of Correct Use of Partial Order:
```python
poset = partial_order(dependencies=[(A, B), (B, C)])
```

Example of Incorrect Use of Partial Order:
```python
poset_1 partial_order(dependencies=[(B, C)])
poset_2 = partial_order(dependencies=[(A, poset)])
```

Please use few-shots learning. These are few illustrating shots extended with common errors that you should avoid for each example:
Process description for example 1:
in this process, you can either do 'a' or 'b'. If 'a' is selected, then it can be repeated. After completing 'a' or 'b', 'c' may be executed. c is always followed by 'd'. Finally another execution of 'a' is performed. The whole process is optional and can be skipped.
Process model for example 1:
```python
from utils.model_generation import ModelGenerator
gen = ModelGenerator()
a = gen.activity('a')
b = gen.activity('b')
a_loop = gen.loop(do=a, redo=None)
choice_1 = gen.xor(a_loop, b)
c = gen.activity('c')
d = gen.activity('d')
poset_c_d = gen.partial_order(dependencies=[(c, d)])
skippable_c_d = gen.xor(poset_c_d, None)
a_copy = a.copy()
poset_1 = gen.partial_order(dependencies=[(choice_1, skippable_c_d), (skippable_c_d, a_copy)])
skippable_1 = gen.xor(poset_1, None)
final_model = skippable_1
```
Common errors to avoid for example 1:
a common error for this process is to add a sequential dependency 'd -> a' without creating a copy of 'a'. This would violate the reflexivity of the partial order.
Process description for example 2:
in this process, you can either do 'a' or 'b'. If 'a' is selected, then it can be repeated. After completing 'a' or 'b', 'c' is executed, followed by 'd'. Finally, the process either ends or goes back to 'a'.
Process model for example 2:
```python
from utils.model_generation import ModelGenerator
gen = ModelGenerator()
a = gen.activity('a')
b = gen.activity('b')
a_loop = gen.loop(do=a, redo=None)
choice_1 = gen.xor(a_loop, b)
c = gen.activity('c')
d = gen.activity('d')
poset_c_d = gen.partial_order(dependencies=[(c, d)])
skippable_c_d = gen.xor(poset_c_d, None)
poset_1 = gen.partial_order(dependencies=[(choice_1, skippable_c_d)])
loop_back = gen.loop(do=poset_1, redo=None)
final_model = loop_back
```
Common errors to avoid for example 2:
a common error for this process is to add a sequential dependency 'd -> a' or 'd -> a.copy()' instead of creating the loop 'loop_back'. 'Going back' indicates the whole process should be repeatable.
Process description for example 3:
inventory management can proceed through restocking items or fulfilling orders. Restocking can be performed as often as necessary. Following either restocking or order fulfillment, an inventory audit is carried out. If unexpected behavior is detected in the inventory audit, then a data analysis is performed. Additionally, urgent restocking needs can bypass regular restocking and order fulfillment processes directly leading to the inventory audit. This entire process is modular and can be repeated or skipped based on operational requirements.
Process model for example 3:
```python
from utils.model_generation import ModelGenerator
gen = ModelGenerator()
restock = gen.activity('restock items')
loop_1 = gen.loop(do=restock, redo=None)
fulfil = gen.activity('fulfill orders')
choice_1 = gen.xor(loop_1, fulfil)
urgent_restock = gen.activity('urgent restock')
choice_2 = gen.xor(choice_1, urgent_restock)
inventory_audit = gen.activity('inventory audit')
data_analysis = gen.activity('data analysis')
optional_data_analysis = gen.xor(data_analysis, None)
poset_1 = gen.partial_order(dependencies=[(choice_2, inventory_audit), (inventory_audit, optional_data_analysis)])
final_skip_loop = gen.loop(do=None, redo=poset_1)
final_model = final_skip_loop
```
Common errors to avoid for example 3:
a common error for this process is to copy 'inventory_audit'.
Process description for example 4:
This enhanced payroll process allows for a high degree of customization and adaptation to specific requirements. Employees' time can be tracked with the option to repeat this step as needed. Pay calculations follows, incorporating diverse factors such as overtime, bonuses, and deductions. Subsequently, the process facilitates the issuance of payments and the generation of detailed reports.
Process model for example 4:
```python
from utils.model_generation import ModelGenerator
gen = ModelGenerator()
track_time = gen.activity('track time')
activity_1_self_loop = gen.loop(do=track_time, redo=None)
activity_2 = gen.activity('calculate pay')
activity_3 = gen.activity('issue payments')
activity_4 = gen.activity('generate reports')
poset = gen.partial_order(
    dependencies=[(activity_1_self_loop, activity_2), (activity_2, activity_3), (activity_2, activity_4)])
final_model = poset
```
Common errors to avoid for example 4:
a common error for this process is to model a choice between activity_3 and activity_4 instead of the concurrency.
Process description for example 5:
This system combines 4 parallel subprocesses, i.e., that are executed independently/at the same time. The first process starts with A followed by B then a choice of C and D. The second process consists of a single activity E which can be repeated but must be executed at least once. The third process consists of the activity F, which can be repeated or skipped. The last process contains the parallel activities G, H, I, J with the constrains that I must precede J and H must precede I
Process model for example 5:
```python
from utils.model_generation import ModelGenerator
gen = ModelGenerator()

# subprocess 1
a = gen.activity('a')
b = gen.activity('b')
choice_c_d = gen.xor(gen.activity('c'), gen.activity('d'))

# subprocess 2
unskippable_self_loop_e = gen.loop(do=gen.activity('e'), redo=None)

# subprocess 3
skippable_self_loop_f = gen.loop(do=None, redo=gen.activity('f'))

# subprocess 4
g = gen.activity('g')
h = gen.activity('h')
i = gen.activity('i')
j = gen.activity('j')

# combine all subprocesses
final_model = gen.partial_order(
    dependencies=[(a, b), (b, choice_c_d), (unskippable_self_loop_e,), (skippable_self_loop_f,), (g,), (h, i),
                  (i, j)])
```
Common errors to avoid for example 5:
a common error for this process is to create partial orders for some subprocesses, then trying to add a partial order as a child of another partial order.
Process description for example 6:
A customer brings in a defective computer and the CRS checks the defect and hands out a repair cost calculation back. If the customer decides that the costs are acceptable , the process continues , otherwise she takes her computer home unrepaired. The ongoing repair consists of two activities , which are executed , in an arbitrary order. The first activity is to check and repair the hardware , whereas the second activity checks and configures the software. After each of these activities , the proper system functionality is tested. If an error is detected another arbitrary repair activity is executed , otherwise the repair is finished.
Process model for example 6:
```python
from utils.model_generation import ModelGenerator
gen = ModelGenerator()
defect_check = gen.activity('Check defect')
cost_calculation = gen.activity('Calculate repair costs')
cancel = gen.activity('Cancel and give computer unrepaired')
repair_hardware = gen.activity('Check and repair the hardware')
repair_software = gen.activity('Check and configure the software')
test_functionality_after_hardware_repair = gen.activity('Test system functionality')
test_functionality_after_software_repair = gen.activity('Test system functionality')
additional_hardware_repair = gen.xor(gen.activity('Perform additional hardware repairs'), None)
additional_software_repair = gen.xor(gen.activity('Perform additional software repairs'), None)
finish_repair = gen.activity('Finish repair')

hardware_repair_order_dependencies = [
    (repair_hardware, test_functionality_after_hardware_repair),
    (test_functionality_after_hardware_repair, additional_hardware_repair)]

software_repair_order_dependencies = [
    (repair_software, test_functionality_after_software_repair),
    (test_functionality_after_software_repair, additional_software_repair)]

poset_full_repair = gen.partial_order(
    dependencies=hardware_repair_order_dependencies + software_repair_order_dependencies +
                 [(additional_software_repair, finish_repair), (additional_hardware_repair, finish_repair)])

# choice between canceling or starting the repair process
choice = gen.xor(cancel, poset_full_repair)

# final model
final_model = gen.partial_order(dependencies=[(defect_check, cost_calculation), (cost_calculation, choice)])

```
Common errors to avoid for example 6:
a common error for this process is to create partial orders for some subprocesses, then trying to add a partial order as a child of another partial order. Another very important error you should avoid is to create a local choice between 'cancel' and some local activity (e.g., 'continue process') instead of modeling a choice between 'cancel' and the rest of the process.
Process description for example 7:
A small company manufactures customized bicycles. Whenever the sales department receives an order , a new process instance is created. A member of the sales department can then reject or accept the order for a customized bike. In the former case , the process instance is finished. In the latter case , the storehouse and the engineering department are informed. The storehouse immediately processes the part list of the order and checks the required quantity of each part. If the part is available in-house , it is reserved. If it is not available , it is back-ordered. This procedure is repeated for each item on the part list. In the meantime, the engineering department prepares everything for the assembling of the ordered bicycle. If the storehouse has successfully reserved or back-ordered every item of the part list and the preparation activity has finished, the engineering department assembles the bicycle. Afterwards , the sales department ships the bicycle to the customer and finishes the process instance .
Process model for example 7:
```python
from utils.model_generation import ModelGenerator
gen = ModelGenerator()
create_process = gen.activity('Create process instance')
reject_order = gen.activity('Reject order')
accept_order = gen.activity('Accept order')
inform = gen.activity('Inform storehouse and engineering department')
process_part_list = gen.activity('Process part list')
check_part = gen.activity('Check required quantity of the part')
reserve = gen.activity('Reserve part')
back_order = gen.activity('Back-order part')
prepare_assembly = gen.activity('Prepare bicycle assembly')
assemble_bicycle = gen.activity('Assemble bicycle')
ship_bicycle = gen.activity('Ship bicycle')
finish_process = gen.activity('Finish process instance')

check_reserve = gen.xor(reserve, back_order)

single_part = gen.partial_order(dependencies=[(check_part, check_reserve)])
part_loop = gen.loop(do=single_part, redo=None)

accept_poset = gen.partial_order(
    dependencies=[(accept_order, inform), (inform, process_part_list),
                  (inform, prepare_assembly), (process_part_list, part_loop),
                  (part_loop, assemble_bicycle), (prepare_assembly, assemble_bicycle),
                  (assemble_bicycle, ship_bicycle)])

choice_accept_reject = gen.xor(accept_poset, reject_order)

final_model = gen.partial_order(
    dependencies=[(create_process, choice_accept_reject), (choice_accept_reject, finish_process)])

```
Common errors to avoid for example 7:
a common error for this process is to create a local choice between 'reject_order' and 'accept_order' instead of modeling a choice between 'reject_order' and the complete complex subprocess that is executed in case the order is accepted ('accept_poset'). Although the text says there is a choice between accepting or rejecting the order, you should derive from your understanding of the context that this choice also includes all activities that are executed after accepting an order.
Process description for example 8:
A and B can happen in any order (concurrent). C and D can happen in any order. A precedes both C and D. B precedes D
Process model for example 8:
```python
from utils.model_generation import ModelGenerator
gen = ModelGenerator()
a = gen.activity('A')
b = gen.activity('B')
c = gen.activity('C')
d = gen.activity('D')
final_model = gen.partial_order(dependencies=[(a, c), (a, d), (b, d)])
```
Common errors to avoid for example 8:
a common error for this process is to generate a first partial order for modeling the concurrency between 'A' and 'B', then a second partial order to model the concurrency between 'C' and 'D', then combining these two partial orders with a large partial that has a sequential dependency from the first order to the second one. This behavior is not justified and it will imply a wrong dependency ('B' -> 'C'); 'B' and 'C' should remain independent in the correct partial order.

At the end of your response provide a single Python code snippet (i.e., staring with '```python') that contains the full final code.

This is the process description: Consider a process for purchasing items from an online shop. The user starts an order by logging in to their account. Then, the user simultaneously selects the items to purchase and sets a payment method. Afterward, the user either pays or completes an installment agreement. After selecting the items, the user chooses between multiple options for a free reward. Since the reward value depends on the purchase value, this step is done after selecting the items, but it is independent of the payment activities. Finally, the items are delivered. The user has the right to return items for exchange. Every time items are returned, a new delivery is made.