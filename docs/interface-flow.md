## Interface Flow Diagram (IOS/Android/Browser)
```mermaid
flowchart TD
    A(Start) --> AA[Init Layout]
    subgraph Splash Screen
      AA --> AB{isRegistered}
      subgraph Device Registration
        AB --> |No| AC[Register RPC]
      end
      AC --> AD[Startup calls]
      AD --> AE{Check for location permission}
      AB --> |Yes| AD
      AE --> |Yes| AF[Get Location]
      AE --> |No| AG[Error Display]
      AF --> AH{Is User logged in}
      AG --> |On Retry| AD
      AH --> |Yes| AI[Refresh access tokens]
      AH --> |No| AJ{Check for login using Google Signin}
      AJ --> |on Error| AG
      AI --> AK[GET user Data]
      AJ --> |Sign in| AL[Get Google User Data]
      AL --> AM[Do App Login]
      AM --> AN{Check for New Login}
      AN --> |No| AK
    end
    AN --> |Yes| AAA
    AK --> BA
    AJ --> |Skip| BA
    AAB --> |on Confirm Data| BA
    subgraph New Login Screen
      AAA[Init layout] --> AAB[Update/Confirm with User profile data]
    end
    subgraph Dashboard Screen
      BA[Init layout]
    end
```