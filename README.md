# HealthReminderDSL
A Domain Specific Language that aids all computer users with timed reminders to carry out healthy habits such as stretching and hydrating


Why HealthReminderDSL? :
Spending my whole lifetime on computers and other screen based devices, along with my passion for holistic wellbeing and health, I felt this would be the best domain specific language to base the project upon.

In the throes of hard work or fun, many users forget the basics of caring for their own health and this language aims to provide a general health reminder using time, intervals and conditions to aid our health in the long term.

The DSL is aimed at non programmer users, creating its own Syntax and grammar.

Many usual wellbeing and reminder apps seem conceptually simple, such as:

Every 60 minutes get up and stretch.
Every morning at 9h, take this medication.

Putting these in a programming language requires too much extra code and timers that can be unrelated to the problem domain, hence:

Declarative syntax for reminders that exposes only domain relevant concepts.

Examples: (to be improved or reiterated)

reminder "Stretch" {
  every: 60min
  message: "Stand up and stretch your arms"
}

or - 

reminder "Medication" {
  at: "09:00"
  message: "Take vitamin D"

}

With this design, users have the freedom to choose what happens instead of worrying about how all this shall be implemented, all thanks to our DSL.


__________________________

Progress Update: April 6th 2026:

The project has been updated from a basic parser to a state aware interpreter,

- updated the health.tx grammar to include Medication entities. Now reminders can point to specific medication using textX's cross referencring capabilities.

- implemented an interdependency check, checking the relationship between different actions. in the latest update for example , we verify that X amount of time has passed since a medication was taken before triggering a reminder
____________________________

Progress Update: April 7th 2026:

The project now triggers system notification alerts.

- installed plyer for notification framework

-using datetime now lets the system distinguish and show SAFE or BLOCKED states based on the user history

- integrated datetime logic to track when medication was last taken to allow real time constraint handling.

Now the dsl is two-tier structured, 
we have global entities defining the medication and conditional reminders to support the internal logic (if) and external dependancies (after) 	

_____________________________

Progress Update: April 11th 2026:

- Established a unit testing with pytest. This allows for Automated Verification of the Meta-model and grammar, ensuring that new features do not introduce regressions in the parser.

- Migrated project configuration to a pyproject.toml file. This standardizes the build system and dependency management, replacing fragmented setup scripts with a unified, declarative configuration.

- Integrated the UV tool for virtual environment syncing and reproducable builds.

- With UV tools implemented here is a reminder on how to run the project:

How to Run:
Install UV: pip install uv

Sync Environment: uv sync

Run the Interpreter: uv run python main.py

Run Tests: uv run pytest

_____________________________

Progress Update: April 13th 2026:

- Expanded the grammar to include a Conflict entity. This allows the DSL to handle safety-critical relationships between medications (e.g., "Do not mix Aspirin with Ibuprofen").

___________________________

Progress Update: April 17th 2026:

- Developed a dedicated web application (app.py) that allows users to interact with the DSL without touching the underlying Python source code.

- Integrated a "Temporal State Slider" that allows for the simulation of time-sensitive scenarios.

- The UI provides immediate syntax validation feedback. The interpreter provides a clear error trace; otherwise, it confirms a "Success" state and triggers the native OS notifications.

- Fulfills the core DSL goal of being accessible to "Domain Experts" (healthcare providers/users) rather than just programmers.

___________________________

Progress Update: April 22nd 2026:

- Added color syntax through pythons own syntax coloring
