## Interface Flow Diagram (IOS/Android/Browser)
```mermaid
flowchart TD
    A(Start) --> B
    subgraph Splash Screen
    B[Init Layout] --> C
    subgraph Device Registration
        C{isRegistered} --> |No| D[Register RPC]
    end
    D --> K[GET user Data]
  end
    K --> Y
  subgraph Dashboard Screen
    Y[Init layout]
  end
```