## Flow Diagram
```mermaid
flowchart TD
  A[User] --> B{Is a Player?}
  C[Admin] --> |1.Creates| D[Tournament]
  B -->|No| E[Register Player]
  -->B
  B -->|Yes| F[Player]
  F -->|2.Registers| D
  C -->|3.Starts| G[Auction]
  G -->|4.Assigns| H[Team]
  D --> G
  I[System] -->|5.Generates| J[Match]
  H -->|Between| J
  C -->|6.Assigns| K[Referee]
  K -->|7.Scores| J
  J -->|8.notifies| I
```
## State Diagram

```mermaid
stateDiagram-v2
  [*] --> RegisteringPlayer
  [*] --> CreatingTournament
  CreatingTournament --> OpensForplayerRegistration
  RegisteringPlayer --> PlayerApproval
  PlayerApproval --> PlayerConfirmation
  PlayerConfirmation --> RegistersForTournament
  OpensForplayerRegistration --> RegistersForTournament
  RegistersForTournament --> StartsAuctions
  RegistersForTournament --> TeamPlayerSelection
  StartsAuctions --> TeamPlayerSelection
  TeamPlayerSelection --> GeneratesFixtures
  GeneratesFixtures --> RefereesAssigned
  RefereesAssigned --> MatchStarts
  MatchStarts --> StartScoring
  StartScoring --> UpdatesResults
  UpdatesResults --> [*]
```

## ER Diagram

```mermaid
erDiagram
  USER ||--|| PLAYER: IS
  TOURNAMENT }|--|{ MATCH: HAS
  PLAYER }|--|{ TOURNAMENT: Registers
  PLAYER }|--|{ MATCH: Plays
  AWARD }|--|{ TOURNAMENT: HAS
  EVENT }|--|{ TOURNAMENT: HAS
```

## Class Diagram

```mermaid
classDiagram
  class User{
    +String id
    +String name
    +String displayPicture
    +String IdToken
    +Player player
  }
  class Player{
    +String id
    +Integer jerseyNo
    +String jerseyName
    +Integer jerseySize
    +Integer shoeSize
    +Float height
    +Float weight
    +date DateOfBirth
    +Location location
  }
  class Tournament{
    +String id
    +String name
    +String logo
    +Location location
    +Timestamp start
    +Timestamp end
    +starts()
    +updatesResults()
  }
  class Team{
    +String id
    +String name
    +String logo
    +Tournament tournament
    +Integer played
    +Integer won
    +Integer point
    +markWon()
    +markLost()
  }
  class Event{
    REGU, QUAD, TEAM, DOUBLES
  }
  class TEvent{
    +String id
    +String name
    +Event event
    +Tournament tournament
  }
  class Match{
    +String id
    +String stagelevel
    +TEvent event
    +Timestamp start
    +Timestamp end
    +Location location
    +Team a
    +Team b
    +markScores()
  }
  class Award{
    +Tournament tournament
    +Player player
    +String name
  }
```

## User Diagram

```mermaid
sequenceDiagram
  Signed in User->>Player: Register
  Admin->>Player: Approves
  note right of Admin: Creates Tournament
  System->>Player: notifies
  System->>(Signed/Unsigned users) Viewers: notifies
  note right of Player: Registers
  note right of Admin: Starts Auction or team selecttion
  note right of System: Generates fixtures
  System->>(Signed/Unsigned users) Viewers: notifies
  Admin->>Referee: Assigns to match
  note right of Admin: Starts Match
  note right of Referee: Scores
  note right of System: Updates results
  System->>(Signed/Unsigned users) Viewers: notifies
```

## C4 Diagram

```mermaid
C4Context
  title System (High Level) Design
  
  Person_Ext(customerA, "Viewer", "Client: Android, Ios, Web")
  
  Boundary(b1, "Data System", "Stores all of the information about players, tournaments, matches, etc.") {  
    Person(customerB, "Scorer")
    Person(customerC, "Meta Scorer") 
    Person(customerD, "Player") 
    Person(customerE, "Admin")
  
    System(SystemA, "Tournament")
    System(SystemB, "match")
    System(SystemC, "Auction")
    
    SystemDb(SystemE, "Data analysis Engine")
    SystemDb(SystemF, "Database")
  
    Boundary(b2, "Notification System", "The internal kafka messaging system.") {
      SystemQueue(SystemAA, "Tournament Queue")
      SystemQueue(SystemAB, "Match Point Queue")
      SystemQueue(SystemAC, "Auction Queue")
    }
  }
  
  Rel(customerB, SystemB, "Scores")
  Rel(customerC, SystemB, "Marks player actions")
  Rel(SystemB, SystemAB, "Event pushed")
  Rel(customerE, SystemA, "Creates")
  Rel(SystemA, SystemAA, "Event pushed")
  Rel(SystemA, SystemB, "Generate")
  Rel(SystemB, SystemAB, "Event pushed")
  Rel(customerD, SystemA, "Registers")
  Rel(customerE, SystemC, "Starts")
  Rel(SystemC, SystemAC, "Event pushed")
  
  Rel(SystemAA, customerA, "Notified")
  Rel(SystemAA, customerD, "Notified")
  Rel(SystemAB, customerA, "Notified")
  Rel(SystemAC, customerA, "Notified")
  
  %% BiRel(customerB, SystemA, "Marks player actions")
```
