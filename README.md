# Learning Journal

**Authors**:

- Adrienne Karnoski (adrienne.j.karnoski@gmail.com)

## Routes:

- `/` - the home page and a listing of all journal entries
- `/journal/new-entry` - to create a new entry
- `/journal/{id:\d+}` - the page for an individual journal entry
- `/journal/{id:\d+}/edit-entry` - for editing existing entry


## Set Up and Installation:

- Clone this repository to your local machine.

- Once downloaded, `cd` into the `pyramid_learning_journal` directory.

- Begin a new virtual environment with Python 3 and activate it.

- `cd` into the next `pyramid_learning_journal` directory. It should be at the same level of `setup.py`

- `pip install` this package as well as the `testing` set of extras into your virtual environment.

- `$ initialize_db development.ini` to initialize the database

- `$ pserve development.ini --reload` to serve the application on `http://localhost:6543`

## To Test

- If you have the `testing` extras installed, testing is simple. If you're in the same directory as `setup.py` type the following:

```
$ py.test pyramid-learning-journal
```