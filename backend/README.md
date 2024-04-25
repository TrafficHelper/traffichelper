### Current Requirements
Dev. details:

DevOps:
    Agile w. Back/Front-end independency
    Client-Server model

Env.:
    >= Python 3.12
    >= PyCharm Community 2024.1 w. Github integration

Dependencies:
    application.py: copy, datetime, math, queue

Plugins:
    Mermaid(Chart) for (&MD) rendering
    IdeaVim editing
    CTAN AMS-LaTeX math typesetting
    CSV Editor 3.3.0-241 (https://github.com/SeeSharpSoft/intellij-csv-validator)

### Disclaimer

All caveats and shortcomings of the application go here:
- It may not provide optimal solutions to user queries, those being an NP-Hard problem
- The application is greatly data-driven and is thus limited by the input data in its predictions
    - To give more accurate predictions, it must be given more updated data
- The application possesses internal consistency but is limited by the data's consistency.

### Structure

Traffic Application Backend:

Data: (Ottawa) Traffic GIS [OpenOttawa,]
- File: Pertinent Information
- RoadCenterlines.csv: The list of all roads and intersections in Ottawa(&boundaries)
- TrafficCollisionData.csv: The list of

Code:

Primary functionality:

User: Vehicle, start & end Node, Cost(safety=Accident risk, distance, time), leave Time, avoid Edges, (Weather), #Path = list[Path] # Given number of best paths from start to end points beginning at selected time, avoiding particular roads and minimizing cost
Admin:
