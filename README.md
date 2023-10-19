# Habit Tracker

## Installation and Usage

### First time install

1. Clone repository
2. Go into the repository and run `python3 -m venv env` (if `python3` is not found, you might have to use `python` or verify your Python installation)

### Start and setup the virtual environment

1. Run `source env/bin/activate` to start the virtual environment
2. Run `pip install -r requirements.txt` to install the dependencies

### Formatting

For formatting we use [black](https://pypi.org/project/black/).

Run `black src`

### Interracting with the app

## Notes

### When adding dependencies

When adding dependencies, always make sure you are using the virtual environment `source bin/activate`.

1. Add dependency to `requirements.txt`
2. Run `pip install -r requirements.txt` to install dependency
