# Notes

## Standards

Durations: https://en.wikipedia.org/wiki/ISO_8601#Durations
Cron: https://en.wikipedia.org/wiki/Cron

## Considerations

Two programs, one for the habit tracker backend and one for the CLI. They communicate using basic http and uses a config file for port.

## CLI interface

```sh
# Creates a habit based on a cron
main.py create_habit --name "Some Habit" --description "blah blah blah" --cron "5 4 * * *" --lifetime "1h2m"
# Creates a habit based on an interval
main.py create_habit --name "Some Habit" --description "blah blah blah" --interval "3d" --lifetime "1h2m"
# List all habits as a table
main.py list_habits # id: uuid ...
# List all habits as json
main.py list_habits --json # [{id:uuid, ...}]
# List all habits as json and export it to file
main.py list_habits --json > export.json
# Deactivate a habit for tracking
main.py deactivate --name 

```