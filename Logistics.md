flowchart TD
    %% Styling
    classDef comp fill:#f9f,stroke:#333,stroke-width:2px;
    classDef db fill:#ff9,stroke:#333,stroke-width:2px,shape:cylinder;

    subgraph Clients
        WebApp[Web Application]:::comp
        MobApp[Mobile App]:::comp
    end

    subgraph Backend_Infrastructure [Backend Infrastructure]
        Gateway[API Gateway]:::comp
        Core[Backend Core Logic]:::comp
        Opt[Route Optimizer]:::comp
        Ware[Warehouse Module]:::comp
        Notify[Notification Service]:::comp
    end

    DB[(Main Database)]:::db
    
    subgraph External_Systems [External Integrations]
        ExtCourier[Courier APIs]:::comp
        ExtPay[Payment Gateway]:::comp
    end

    %% Relationships
    WebApp -->|REST API| Gateway
    MobApp -->|REST API| Gateway
    
    Gateway -->|HTTP| Core
    Core -->|SQL| DB
    
    Core --> Opt
    Core --> Ware
    Core --> Notify
    
    Core -.->|Webhook| ExtCourier
    Core -.->|Transaction| ExtPay
