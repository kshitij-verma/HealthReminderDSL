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



