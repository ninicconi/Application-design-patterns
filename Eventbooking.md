```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant System
    participant Gateway as Payment Gateway
    actor Admin as Venue Admin
    actor Contractor
    actor Manager

    Client->>System: Request Availability
    activate System
    
    alt Venue Unavailable
        System-->>Client: Suggest different dates
    else Venue Available
        System-->>Client: Show Price & Conditions
        
        Client->>System: Confirm Booking
        System->>Gateway: Request Pre-payment
        activate Gateway
        
        alt Payment Failed
            Gateway-->>System: Declined
            System-->>Client: Notify: Failed, Retry
        else Payment Successful
            Gateway-->>System: Approved
            deactivate Gateway
            
            System-->>Client: Booking Confirmed
            System-->>Admin: New Booking Alert
            
            Admin->>System: Create Task List
            
            par Notify Contractors
                System->>Contractor: Notify Task: Decor
            and 
                System->>Contractor: Notify Task: Catering
            end
            
            Contractor-->>System: Confirm Completion
            System-->>Admin: Send Report
            
            Note over Client, System: Event Takes Place
            
            System->>Client: Request Feedback
            Client->>System: Submit Feedback
            System->>Manager: Send Performance Report
        end
    end
    deactivate System
