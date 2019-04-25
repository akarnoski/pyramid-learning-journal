# Learning Journal

A simple Pyramid app for listing and displaying expenses.

**Authors:**:Adrienne Karnoski, [John Jensen](https://github.com/jensjoh01)

**Deployed Site:** https://macabre-caverns.herokuapp.com/

## App Navigation:

| Route | Name | Description |
| --- | --- | --- |
| '/' | home | shows a list of journal entries with just the title and date created |
| '/new-entry' | create | an HTML form page will be used to create a new entry. The title and test of the entry should be inputs in this form, empty at first |
| '/post/{id:\d+}' | detail | shows a singe entry by id |
| 'edit-entry/{id:\d+}/edit' | edit | HTML form page that will be ised to edit an existing entry |

- `/` - the home page and a listing of all journal entries
- `/journal/new-entry` - to create a new entry
- `/journal/{id:\d+}` - the page for an individual journal entry
- `/journal/{id:\d+}/edit-entry` - for editing existing entry


## Set Up and Installation:

Clone this repository to your local machine.

```
$ git clone https://github.com/adriennekarnoski/pyramid-learning-journal.git
```

Once downloaded, change directories into the `pyramid_learning_journal` directory.

```
$ cd pyramid_learning_journal
```

Begin a new virtual environment with Python 3 and activate it.

```
pyramid_learning_journal $ python3 -m venv ENV
pyramid_learning_journal $ source ENV/bin/activate
```

`pip install` this package as well as the testing set of extras into your virtual environment.

```
(ENV) pyramid_learning_journal $ pip install -e .[testing]
```

Create a postgres database for use with this application.Export an environment variable pointing to this location of youe database
- `$ initialize_db development.ini` to initialize the database, populating with random models.

- `$ pserve development.ini --reload` to serve the application on `http://localhost:6543`

## To Test

- If you have the `testing` extras installed, testing is simple. If you're in the same directory as `setup.py` type the following:

```
$ py.test expense_tracker
```