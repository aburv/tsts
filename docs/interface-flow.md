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
    subgraph New Login Screen - Mobile screen
      AAA[Init layout] --> AAB[Confirm with User profile info]
      AAB --> |on Confirm Data| AAC[select user role]
      AAC --> |on Player select| AAD
      subgraph Player Registration form
        AAD --> |yes| AAAA[Screen 1 Player user details]
        AAAA --> AAAB[Screen 2 Player details]
        AAAB --> AAAC[Screen 3 Player partcipation details]
        AAAC --> |for all tournaments|AAAD
        AAAD --> AAAE[Screen 4 Player preview]
      end
    end
    AAAE --> |on Done| BA
    subgraph Dashboard Screen
      BA[Init layout]
    end
    BA --> C[onPlayerClick]
    C --> CA
    B(On Player click/URL) --> CA[Init layout]
    subgraph Player Screen
      CA --> CB[Data calls]
      CB --> CC[Creates TABS]
    end
```