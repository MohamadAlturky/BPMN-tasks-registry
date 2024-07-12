Business Process Model and Notation (BPMN) is a graphical representation for specifying business processes in a business process model. It provides a standard way to map out the steps in a business process, allowing for clear communication among stakeholders. BPMN defines various types of activities, which are fundamental elements used to describe the tasks or work performed within a business process. Here's a detailed explanation of BPMN activities:

### 1. **Tasks**

A **Task** represents a single unit of work that is performed by a person, system, or both. It is the most basic activity within BPMN. Tasks can be further categorized into various types, depending on their specific purpose and the type of work being performed:

- **Service Task**: Represents a task that uses some sort of service, such as a web service or an automated application.
- **User Task**: Represents a task that is performed by a human user with the assistance of a software application.
- **Manual Task**: A task that is performed without the aid of any business process execution or any application.
- **Business Rule Task**: A task that provides a mechanism for the business process to provide input to a business rules engine and get the output of calculations that the business rules engine might provide.
- **Script Task**: A task that is executed by a business process engine. The engine will interpret or run the script.
- **Send Task**: Represents the act of sending a message to an external participant.
- **Receive Task**: Represents the act of receiving a message from an external participant.

### 2. **Sub-processes**

A **Sub-process** is a compound activity that can be broken down into a finer level of detail. It encapsulates a series of tasks and activities into a single activity. Sub-processes help in organizing complex processes by breaking them into manageable chunks.

- **Embedded Sub-process**: A sub-process that is part of the parent process and cannot be reused independently.
- **Reusable Sub-process (Call Activity)**: A sub-process that is defined independently of the parent process and can be reused in multiple processes.

### 3. **Call Activities**

A **Call Activity** is a type of activity that allows the inclusion of reusable sub-processes or global tasks within a process. It provides a way to call another process or sub-process that is defined globally, allowing for modularization and reuse of common process elements.

### 4. **Transactions**

A **Transaction** is a specialized type of sub-process that represents a set of activities that logically belong together, and that must all complete successfully for the transaction to be considered successful. If any of the activities within the transaction fail, the process can be rolled back to maintain consistency.

### 5. **Event Sub-processes**

An **Event Sub-process** is a sub-process that is triggered by an event and can interrupt the main process flow or execute in parallel. It is used to handle events that may occur during the execution of the parent process.

### 6. **Loop, Multi-instance, and Ad Hoc Activities**

- **Loop Activity**: An activity that repeats based on a looping condition.
- **Multi-instance Activity**: An activity that can be performed multiple times, either in parallel or sequentially, based on certain conditions or for a specified number of instances.
- **Ad Hoc Activity**: An activity where the sequence of steps is not pre-defined, allowing for more flexibility in execution.

### Visual Representation

- **Tasks** are typically represented as rounded rectangles with an icon inside indicating the type of task.
- **Sub-processes** are represented as rounded rectangles with a plus sign (+) at the bottom center, indicating that it can be expanded to show the detailed flow within.
- **Call Activities** are represented similarly to tasks but with a thick border, indicating that they reference an external process.
- **Transactions** are shown as rounded rectangles with a double-lined border.
- **Event Sub-processes** are shown with a dashed border to distinguish them from regular sub-processes.
- **Loop and Multi-instance** markers are placed at the bottom center of the activity symbol, showing looping or parallel/sequential execution.

### Example Diagram

Here is a simple BPMN diagram illustrating different types of activities:

```plaintext
+--------------------------------+
| Start Event                    |
+--------------------------------+
          |
          v
+--------------------------------+
| User Task: Approve Request     |
+--------------------------------+
          |
          v
+--------------------------------+
| Service Task: Process Payment  |
+--------------------------------+
          |
          v
+--------------------------------+
| Call Activity: Notify Customer |
+--------------------------------+
          |
          v
+--------------------------------+
| End Event                      |
+--------------------------------+
```

In this example:

- The process starts with a **Start Event**.
- A **User Task** represents a manual approval step.
- A **Service Task** automates the payment processing.
- A **Call Activity** invokes a separate process to notify the customer.
- The process ends with an **End Event**.

Understanding these BPMN activities and their representations helps in effectively modeling and analyzing business processes for better management and optimization.
