## Interface Flow Diagram (IOS/Android/Browser)
```mermaid
flowchart TD
    A(Start) --> B
    subgraph Splash Screen
      B[Init Layout] --> C
      subgraph Device Registration
        C{isRegistered} --> |No| D[Register RPC]
      end
      D --> E{Check for location permission}
      C --> |Yes| E
      E --> |Yes| F[Get Location]
      E --> |No| G[Error Display]
      F --> H{Is User logged in}
      G --> |On Retry| B
      H --> |Yes| I[Refresh access tokens]
      H --> |No| J{Check for login using Google Signin}
      J --> |on Error| G
      I --> K[GET user Data]
      J --> |Sign in| L[Get Google User Data]
      L --> M[Do App Login]
      M --> N{Check for New Login}
      N --> |No| K
    end
    N --> |Yes| U
    K --> Y
    J --> |Skip| Y
    V --> |on Confirm Data| Y
    subgraph New Login Screen
      U[Init layout] --> V[Update/Confirm with User profile data]
    end
    subgraph Dashboard Screen
      Y[Init layout]
    end
```