# Habit Tracker

## Installation and Usage

### First time install

1. Clone repository
2. Go into the repository and run `python3 -m venv env` (if `python3` is not found, you might have to use `python` or verify your Python installation)

### Start and setup the virtual environment

1. Run `source env/bin/activate` to start the virtual environment
2. Run `pip install -r requirements.txt` to install the dependencies

### Starting the app

1. In one terminal window (don't forget to set up virtual env), run `python3 src/main.py`, dont close this terminal and simply leave it in the background
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
