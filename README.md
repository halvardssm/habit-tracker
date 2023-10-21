# Habit Tracker

## Installation and Usage

### First time install

1. Clone repository
2. Go into the repository and run `python3 -m venv env` (if `python3` is not found, you might have to use `python` or verify your Python installation)

### Start and setup the virtual environment

1. Run `source env/bin/activate` to start the virtual environment
2. Run `pip install -r requirements.txt` to install the dependencies

### Starting the app

1. In one terminal window (don't forget to set up virtual env), run `python3 src/main.py`, dont close this terminal and simply leave it in the background. You can provide the argument `--port` to override the port (default 5000).
2. In a new terminal window (don't forget to set up virtual env), run `python3 src/cli.py [command]` with the arguments required
3. Repeat 2 as needeed
4. Once done, close the terminals

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
habit:create        Create a new habit
habit:list          List habits
task:list           List tasks
task:complete       Complete a task
```

### Habit Create

Example:

```
python src/cli.py habit:create --name test --description "test description" --interval P1D --lifetime P2D
```

Options:

```
  -h, --help            show this help message and exit
  --name NAME           The name of the habit to create
  --description DESCRIPTION
                        The description of the habit to create
  --interval INTERVAL   The interval of the habit to create, must follow
                        ISO8601 duration standard
                        (P[n]Y[n]M[n]DT[n]H[n]M[n]S), e.g. P1Y
  --lifetime LIFETIME   The lifetime of the habit to create, must follow
                        ISO8601 duration standard
                        (P[n]Y[n]M[n]DT[n]H[n]M[n]S), e.g. PT1H
  --active ACTIVE       The active of the habit to create, boolean, default
                        false
  --start START         The start of the habit to create, iso format, default
                        now
  --end END             The end of the habit to create, iso format, default 1
                        year from now
```

### Habit List

Example:

```
python src/cli.py habit:list --id 2
```

Options:

```
  -h, --help            show this help message and exit
  --id ID               Filter by id
  --name NAME           Filter by name
  --description DESCRIPTION
                        Filter by description
  --interval INTERVAL   Filter by interval
  --lifetime LIFETIME   Filter by lifetime
  --active ACTIVE       Filter by active
  --start START         Filter by start date
  --end END             Filter by end date
```

### Task List

Example:

```
python src/cli.py task:list --habit_id 2
```

Options:

```
  -h, --help            show this help message and exit
  --habit_id HABIT_ID   Filter by habit id
  --completed COMPLETED
                        Filter by completed
  --start START         Filter by start date
  --end END             Filter by end date
```

### Task Complete

```
python src/cli.py task:complete --id 336
```

Options:

```
  -h, --help  show this help message and exit
  --id ID     The id of the task to complete
```
