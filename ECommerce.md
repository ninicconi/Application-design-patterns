```mermaid
classDiagram
    %% Abstract Class
    class User {
        <<Abstract>>
        -int ID
        -string name
        -string email
        +register()
        +login()
    }

    class Customer {
        -int loyaltyPoints
        +viewHistory()
        +addReview()
    }

    class Administrator {
        -string adminLevel
        +manageUsers()
        +viewLogs()
    }

    class Product {
        -int productID
        -string name
        -double price
        -int stock
        +create()
        +update()
    }

    class Order {
        -int orderID
        -Date date
        -string status
        +placeOrder()
        +cancel()
    }

    class OrderItem {
        -int quantity
        -double price
    }

    class Payment {
        -int paymentID
        -double amount
        +process()
        +refund()
    }

    class Delivery {
        -int deliveryID
        -string status
        +track()
    }

    %% Relationships
    User <|-- Customer
    User <|-- Administrator
    Customer "1" --> "0..*" Order : places
    Order "1" *-- "1..*" OrderItem : contains
    Product "1" --> "0..*" OrderItem : listed in
    Order "1" --> "1" Payment : requires
    Order "1" --> "1" Delivery : triggers
