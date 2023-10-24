# Habit Tracker

## Installation and Usage

### First time install

1. Clone repository
2. Go into the repository and run `python3 -m venv env` (if `python3` is not found, you might have to use `python` or verify your Python installation)

### Start and setup the virtual environment

1. Run `source env/bin/activate` to start the virtual environment
2. Run `pip install -r requirements.txt` to install the dependencies

### Seed example data

1. Run `python src/db_seed.py`

This will seed the database with 5 habits and their tasks with past tasks completed.

### Remove data

Delete the file called `database.db`.

### Starting the app

1. In one terminal window (don't forget to set up virtual env), run `python3 src/main.py`, dont close this terminal and simply leave it in the background. You can provide the argument `--port` to override the port (default 5000).
2. In a new terminal window (don't forget to set up virtual env), run `python3 src/cli.py [command]` with the arguments required
3. Repeat 2 as needeed
4. Once done, close the terminals

### Tests

To run the tests:

1. Start the backend `python3 src/main.py`
2. In a new terminal window, run `python -m unittest discover -s src`

### Formatting

For formatting we use [black](https://pypi.org/project/black/).

Run `black src`

### When adding dependencies

When adding dependencies, always make sure you are using the virtual environment `source env/bin/activate`.

1. Add dependency to `requirements.txt`
2. Run `pip install -r requirements.txt` to install dependency

## CLI Usage

You can use `-h` to display help for the CLI.

Here are the different sub commands:

```
    habits:create       Create a new habit
    habits:list         List habits with filters
    habits:update       Update a habit
    habits:delete       Delete a habit
    tasks:list          List tasks
    tasks:active        List tasks that are active and can be completed
    tasks:complete      Complete a task
    analytics           Query analytics. You can already get a lot of information using the list commands, but this is a
                        central analytics helper.
```

### Examples

#### Habit Create

```
python src/cli.py habits:create --name test --description "test description" --interval P1D --lifetime P2D --active true --start 2023-10-24T08:00:00 --end 2024-12-27T22:00:00
```

#### Habit List

```
python src/cli.py habits:list --id *in(2,3) --name test --description test --interval P1D --lifetime P2D --active true --start <2023-10-24T08:00:00 --end >2024-12-27T22:00:00
```

#### Habit Update

```
python src/cli.py habits:update --id 1 --name test --description "test description" --interval P1D --lifetime P2D --active true --start 2023-10-24T08:00:00 --end 2024-12-27T22:00:00
```

#### Habit Delete

```
python src/cli.py habits:delete --id 1
```

#### Task List

```
python src/cli.py tasks:list --habit_id 2 --completed true --start 2023-10-24T08:00:00 --end 2024-12-27T22:00:00
```

#### Task Active

```
python src/cli.py tasks:active
```

#### Task Complete

```
python src/cli.py tasks:complete --id 336
```

## Analytics

In the case of analytics, there is an endpoint that will wrap around the existing commands and also provides some more.

### Examples

#### List current Habits

```sh
python src/cli.py analytics list_current_habits
```

#### List current Habits and filter by interval

```sh
python src/cli.py analytics list_current_habits --interval P1D
```

#### List longest streaks

```sh
python src/cli.py analytics list_longest_streaks 
```

#### List longest streaks and filter by habit id

```sh
python src/cli.py analytics list_longest_streaks --habit_id 1
```

#### List longest streaks greater than 5

```sh
python src/cli.py analytics list_longest_streaks --streak >5
```

#### Get longest streak

```sh
python src/cli.py analytics get_longest_streak
```

#### Get longest streak and filter by habit id

```sh
python src/cli.py analytics get_longest_streak --habit_id 1
```
