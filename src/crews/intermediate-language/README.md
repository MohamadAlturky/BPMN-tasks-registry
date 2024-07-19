# Example

Pool [Order Processing]
Swimlane [Sales]
Start Event O -> Task [Receive Order]
Task [Receive Order] -> XOR Gateway 1
XOR Gateway 1 -> Condition (Order Valid)
XOR Gateway 1 -> Condition (Order Invalid)
Condition (Order Valid) -> Task [Process Order]
Condition (Order Invalid) -> Event End O

    Swimlane [Inventory]
        Task [Process Order] -> AND Gateway 1
        AND Gateway 1 -> Task [Check Stock]
        AND Gateway 1 -> Task [Update Inventory]
        Task [Check Stock] -> XOR Gateway 2
        XOR Gateway 2 -> Condition (Stock Available)
        XOR Gateway 2 -> Condition (Stock Not Available)
        Condition (Stock Available) -> Task [Reserve Stock]
        Condition (Stock Not Available) -> Task [Notify Sales]

    Swimlane [Shipping]
        Task [Reserve Stock] -> Task [Prepare Shipment]
        Task [Prepare Shipment] -> Task [Ship Order]
        Task [Ship Order] -> Event End O

Actor Mapping:
Sales: [Receive Order, Process Order]
Inventory: [Check Stock, Update Inventory, Reserve Stock, Notify Sales]
Shipping: [Prepare Shipment, Ship Order]
