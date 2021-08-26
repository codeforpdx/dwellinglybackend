# Contributing

## App Architecture

This section describes the structure of the Python backend for the Dwellingly application. This does not cover the React frontend.

Dwellingly is developed using the following tools and extensions:

- [Flask](https://palletsprojects.com/p/flask/) is used for the main web application framework
- [SQLite](https://sqlite.org/index.html) is used for database management ([Postgres](https://www.postgresql.org/) for production)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/14/) is used for object-relational mapping
- [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/) is used for routing to encourage RESTful routes and resources.
- [Marshmallow](https://marshmallow.readthedocs.io/en/stable/) is used for input validation, serialization, and deserialization.
- Flask-Mailman is currently used to send mail and Jinja is used for templating the email messages.
- [Flake8](https://gitlab.com/pycqa/flake8) is currently installed for linting, but it is probably not being used by many contributors. However, we will most likely be using [Black](https://github.com/psf/black) in the future, or a combination of Flake8 for linting and Black for formatting.
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) was recently installed for database migrations. However, while the app is under development, we rebuild the database whenever there is a change.

## Project Environments

The Dwellingly app is developed using the following environments:

- `development`
- `testing`
- `production`

## Testing

We use [pytest](https://docs.pytest.org/en/latest/) for automated testing.

All new functionality, changes in behavior, or bug fixes should be tested.

## Project Components

The three main areas of the application to be familiar with are resources, models, and schemas. The models and resources align respectively with the model and controller components of a Model-View-Controller (MVC) web application. Schemas are used for input validation and deserialization.

There is one more file to be familiar with and that is the `app.py` file. This is the file that executes when the application starts.

The rest of this section will describe the three main areas, and how each of those areas should be tested.

### Models

Models define the database tables, the methods used to fetch data from the database, the tables to create, and what columns to use. They can also contain other methods that relate to the business logic of the application. All models in this application inherit from the BaseModel class, which adds `created_at` and `updated_at` timestamps for all the tables in the database. It also contains methods that are used to find, create, update, and delete database rows. Models can be found in the `models` directory.

#### Testing Models

All models should have unit tests that can be found in the `tests/unit` directory. Each model should have tests that test the inherited methods from the BaseModel to ensure that nothing crazy is inadvertently done to change the behavior of the methods that the BaseModel provides. These are easily implemented using the `base_interface_test` file. Finally, there should be a test for every public method that is defined in the model. This would be the JSON method or any other method defined in the file that is directly used outside of the Models class.

### Schemas

Marshmallow schemas are used primarily for input validation and deserialization. Schemas validate the data that is received by the client at the back end, before the data is inserted into the database or used by other parts of the app. Schemas can be found in the `schemas` directory.

#### Testing Schemas

All schemas should have unit tests, which primarily should be validation tests. This app uses Flask-Marshmallow, which provides an auto-schema that infers some basic validations based on the table definition in the Models class. Any additional validations defined in the schema must be tested. Schema tests can be found in the `tests/schemas` directory. Deserialization should also be tested here when used.

### Resources

Flask-RESTful uses the term "resources" in place of "controllers" in an MVC framework and that is also the term we use in this project.

A resource's main job is to coordinate a response for the incoming request. If data is provided, the resource will send that data to the schema for validation and deserialization. The resource will communicate with the model to query for data or insert/update a table row in the database. Finally, the resource will send a response back to the client. Resources can be found in the `resources` directory.

#### Testing Resources

Each resource will usually have one test for each action (GET, POST, DELETE, etc...). When the Models and Schemas have unit tests, and when the resource uses the models and schemas appropriately, then **generally** only a successful response (The Happy Path) needs to be tested. All other responses that can occur are already tested elsewhere, including validation errors or database rows that cannot be found. Errors such as these should not be tested, as they're already built into the architecture of the app and happen automatically as long as the schemas are used along with the appropriate methods defined in the BaseModel. Tests for the resources can be found in the `tests/integration` directory.

## Installation

NOTE: Default development database is SQLite3. (Optionally setup and use [PostgreSQL](#PostgreSQL-Setup) as the database.)

[Note for Windows users](#Note-For-Windows-Users)

[Mac OS Troubleshooting](#Mac-OS-Troubleshooting)

1. Clone the repo (`git clone https://github.com/codeforpdx/dwellinglybackend.git`)
2. Install [pyenv](https://github.com/pyenv/pyenv) | This step is optional but recommended.
   - With pyenv installed pipenv will automatically install the correct python version.
   - NOTE:
     - If you previously had the project running, but need to upgrade to Python 3.9.6, check out the OS-specific documentation under [Mac OS Troubleshooting](#Mac-OS-Troubleshooting) and [Note for Windows users](#Note-For-Windows-Users)
3. Install [pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today)
   - Note: Pipenv handles the install for all dependencies. Including Python.
   - Please install pipenv according to their docs for your OS.
4. Install dependencies `pipenv run dev-install`
   - Note: Pipenv may prompt you to install Python if it cannot find the correct version on your system. You should select Yes.
   - Note: If you get the error `ImportError: cannot import name 'Feature' from 'setuptools'`, your setuptools version might be at 46 or later. You may be able to get it to work using version 45 (e.g. `pip3 install setuptools==45`)
5. Install our pre-commit hook:
   - Run: `pipenv run pre-commit install`
6. copy the contents of the `.env.example` to a new file called `.env`
   - `cp .env.example .env`
7. Create and Seed the database

   - Run: `pipenv run flask db create`

   - Some other useful commands are:
     - To re-seed the database from scratch run: `pipenv run flask db recreate`
     - To find other database set-up commands run: `pipenv run flask db --help`
     - To drop the database run: `pipenv run flask db drop`

8. Start the server using the flask environment (required every time the project is re-opened):
   - Run: `pipenv run flask run`
   - Run and restart the server on changes: `pipenv run flask run --reload`
9. Test the server and view coverage reports. Use of coverage reporting is recommended to indicate test suite completeness and to locate defunct code in the code base.
   - Run all the tests: `pipenv run pytest --cov .`
     - Run tests in a particular directory: `pipenv run pytest --cov [path to directory]`
       - Example: Just the integration tests: `pipenv run pytest --cov tests/integration`
     - Run tests in a single file : `pipenv run pytest -s [path to test file]`
       - Example: Just the users integration tests: `pipenv run pytest -s tests/integration/test_users.py`
     - Run a specific test in a file: `pipenv run pytest -s [path to test file] -k '[test name]'`
       - Example: Just test_archive_user from the users integration tests: `pipenv run pytest -s tests/integration/test_users.py -k 'test_archive_user'`
   - View detailed coverage reports, with listings for untested lines of code ...
     - As a web page: `pipenv run python view_coverage.py`
     - In the console: `pipenv run view_coverage`
   - Tests can be run automatically after each file save using [pytest-watch](https://pypi.org/project/pytest-watch/). Visit the documentation to learn how to run it for your system. See [PR #72](https://github.com/codeforpdx/dwellinglybackend/pull/72) for a preview of what it can do.
10. (OPTIONAL) Set up your workflow using the [Advanced Setup documentation](./advanced_setup.md)

Queries can be made with the Postman Collection link ( https://www.getpostman.com/collections/a86a292798c7895425e2 )
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/0078de8f58d4ea0b78eb)

### PostgreSQL Setup

1. Install [PostgreSQL](https://www.postgresql.org/download/).
2. Manually create the database.
   - From a linux or mac command line run the following:
     ```shell
      createdb dwellingly_development
      createdb dwellingly_test
     ```
3. Open up `.env` and uncomment the `DEV_DATABASE_URL` and `TEST_DATABASE_URL` env vars.
4. Run `pipenv run flask db create`.

### Note For Windows Users

Python does not come by default for Windows users. Sometimes the PATH variable in Windows will point to the wrong path and you will have trouble running the `python` and `pipenv` commands. If you don't have Python installed then follow these steps. If the steps listed above did not work for you, try the following.

1. Clone the repo (`git clone https://github.com/codeforpdx/dwellinglybackend.git`)
2. Hit the Windows key on your keyboard and type `Microsoft Store`. Click on Microsoft store and search for Python. Download Python from the official Microsoft store. When you are installing **make sure you tick the Add to PATH checkbox [ ]** If you don't do this, it could result in you being unable to run the python or pip / pipenv commands.
3. Once Python is installed, run `pip3 install --user pipenv` If this command doesn't work, try running `python -m pip install --user pipenv`
4. Follow instructions 4-6 from the previous instructions section.

#### Upgrading project to Python 3.9.6 on Windows

To upgrade your pipenv environment to use Python 3.9.6, try the following steps:

1. Navigate to the project folder using the terminal and run `pipenv --rm` to remove the existing virtual environment.
2. Download Python 3.9.6 from https://www.python.org/downloads/ and install by following the instructions on the installer. Note: You do **not** need to add this version of Python to your PATH if you do not intend to use it as your default Python version.
3. Once the new version of Python is installed, open your terminal to the `dwellinglybackend` directory and run the following command: `pipenv run dev-install` Pipenv should create the new virtual environment for you using Python 3.9.6

#### Still having issues on Windows?

If you are still having issues or if your command prompt is throwing an error that says `python is not a command` or `pip is not a command`, it is most likely a pathing issue where the ENV variable is pointing to the wrong directory. To try to troubleshoot, I suggest following this guide: ( https://github.com/LambdaSchool/CS-Wiki/wiki/Installing-Python-3-and-pipenv ).

### Mac-OS-Troubleshooting

Check to see where the Python you're running is located (`which python`). You should see something like `/Users/your_account_shortname/.pyenv/shims/python`.
If you don't see something similar, you may have several versions of Python installed elsewhere (via Anaconda or Homebrew). If (and only if) you'd like to clear out any previous homebrew-based installs, type `brew uninstall --ignore-dependencies python3 && brew uninstall --ignore-dependencies python`.

#### Upgrading project to Python 3.9.6 on MacOS

To upgrade your pipenv environment to use Python 3.9.6, try running the following commands with the terminal opened to the `dwellinglybackend` directory:

```bash
pipenv --rm
brew update && brew upgrade pyenv
pipenv run dev-install
```

### Database migrations.

Database migrations are currently not used. We will start using them soon.

Database migrations are managed through [Alembic](https://alembic.sqlalchemy.org/en/latest/index.html). After making a change to a model, a database migration is necessary.

- The first step is to create a revision: `pipenv run alembic revision --autogenerate -m "message"`
- The second step is to upgrade: `pipenv run alembic upgrade head`

To return to a previous version, a downgrade is necessary. Run:
`pipenv run alembic downgrade -n` where n is the number of versions to downgrade.

To downgrade to the very beginning run: `pipenv run alembic downgrade base`

The reversion are maintained as Python files in ``./migrations/versions/`

### Contributing

How to contribute to this project.

1. Set your origin to https://github.com/codeforpdx/dwellinglybackend.git
2. The Main Branch is Development

```console
~$: git pull origin development
```

3. Branch from Development

```console
~$ git checkout -b <name of branch>
```

(Step #3 creates a new branch titled <name of branch> and navigates you to that branch)

4. Commit your changes (and resolve commit errors)
   - Our pre-commit hook is designed to be strict in order to ensure all code being committed to the codebase is as clean and uniform as possible. Commit errors are a good thing, and completely expected!
   - The pre-commit hook will check your code every time you try to commit. If your code needs re-formatting, that will happen automatically. If you have non-formatting errors in your code, these will be printed to the terminal with the error, filename and line number. You will need to resolve these yourself.
   - After your code has been reformatted and/or you have resolved other errors, you will need to add and commit those files again (because they have been modified).
   - Successful commits can then be pushed to your remote branch like normal.
   - NOTE: If you did not set up pre-commit as described in Step 4 of [Installation](#Installation), our CI will still perform these checks when you make a PR into `development`. If the build fails, you will be asked to push the appropriate changes to your branch before it can be merged.

(For more information on the pre-commit hook, Flake8 and the Black formatter, see the [Advanced Setup documentation](./advanced_setup.md))

#### Updating development branch

To update your development branch with the latest changes:

1. First checkout the development branch if not already checked out.

- Then run: `git checkout development`

2. Pull the latest changes from github down to your local copy.

- Assuming origin is set to the GitHub Code for PDX dev branch run:
- `git pull origin development`

3. After pulling fresh copy it is a good habit to install any new deps and rebuild the database. Run the following two commands:

- `pipenv run dev-install`
- `pipenv run flask db recreate`

4. Finally - run the tests to ensure everything is passing.

- `pipenv run pytest`
