# Habit Tracker Proposal

## Technical Requirements

Following is a list of technical requirements

## Application Architecture

### Options

1. Run the program and interact with the main loop
2. Run a backend and have a separate client interacting with the backend

### Considerations

Option 1 will allow for initial easier development, but might cause problems later down the line if requirements are altered, or futher expansion of the system is needed. Option 2 allows for better flexibility in the future in case a GUI or alternative frontends are needed, and will increase isolation of the applications. 

### Conclusion

Option 2: Run a backend and have a separate client interacting with the backend

## Data Storage

### Options

1. Json file
2. SQLite database
3. MongoDB, MySQL or PostgreSQL

### Considerations

Json is a standard information format and is widely used on the web, the downside is that we will need to recreate what a database already has implemented when we want to adjust data. SQLite is a part of the standard library, and although it requires knowledge of SQL, this is also widely standardized not creating a barrier of future team members and development. A database also scales better than a Json file. Using a fully fledged database like MongoDB is future proofing and scales well, however it is an overkill for the requirements for this app.

### Conclusion

Option 2: SQLite database

## Data Schemas

### Considerations

We should store Habits as 
In addition to the habits that we need
