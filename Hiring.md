```mermaid
flowchart TD
    subgraph Dept_Head [Department Head]
        Start((Start)) --> CreateReq[Create Vacancy Request]
        Rework[Rework Request]
        TechInt[Technical Interview]
    end

    subgraph HR [HR Department]
        CheckReq{Request Valid?}
        Publish[Publish Vacancy]
        Screen[Screen CVs]
        CheckCV{Suitable?}
        HRInt[HR Initial Interview]
        IntPass{Passed Both?}
        Offer[Send Offer]
        NotifyIT[Notify IT]
    end

    subgraph System [System]
        AlertHead[Notify Head: Rework]
        Reject[Send Rejection Email]
        AddDB[Add Employee to DB]
    end

    subgraph Candidate [Candidate]
        Apply[Submit Application]
        Accept[Accept Offer]
    end

    subgraph IT [IT Department]
        Setup[Setup Workstation] --> Stop((End))
    end

    %% Logic Flow
    CreateReq --> CheckReq
    CheckReq -- No --> AlertHead
    AlertHead --> Rework
    Rework --> CheckReq
    CheckReq -- Yes --> Publish
    
    Publish --> Apply
    Apply --> Screen
    Screen --> CheckCV
    
    CheckCV -- No --> Reject
    CheckCV -- Yes --> HRInt
    HRInt --> TechInt
    TechInt --> IntPass
    
    IntPass -- No --> Reject
    IntPass -- Yes --> Offer
    Offer --> Accept
    Accept --> AddDB
    AddDB --> NotifyIT
    NotifyIT --> Setup
    Reject --> Stop
