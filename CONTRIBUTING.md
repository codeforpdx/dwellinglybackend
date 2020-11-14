# Contributing
## Installation
Set up Dwelling Flask Testing Backend (for the first time)
NOTE: Database is SQLite3 via SQLAlchemy

[Note for Windows users](#Note-For-Windows-Users)

[Mac OS Troubleshooting](#Mac-OS-Troubleshooting)

1. Clone the repo (`git clone https://github.com/codeforpdx/dwellinglybackend.git`)
2. Install [pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today)
    - Note: It is not necessary to install python before installing pipenv.
    - Please install pipenv according to their docs for your OS.
3. Install dependencies `pipenv install -d`
   - Note: Pipenv may prompt you to install Python if it cannot find the correct version on your system. You should select Yes.
   - Note: If you get the error `ImportError: cannot import name 'Feature' from 'setuptools'`, your setuptools version might be at 46 or later. You may be able to get it to work using version 45 (e.g. `pip3 install setuptools==45`)
4. copy the contents of the `.env.example` to a new file called `.env`
    - `cp .env.example .env`
5. Create and Seed the database
   - Run: `pipenv run flask db create`
   - To re-seed the database from scratch run: `pipenv run flask db recreate`
   - Look for the file data.db to be created in the root directory
   - To find other database set-up commands run: `pipenv run flask db --help`
   - To drop the database run: `pipenv run flask db drop`
6. Start the server using the flask environment (required every time the project is re-opened):
   - Run: `pipenv run flask run`
   - Run and restart the server on changes: `pipenv run flask run --reload`
7. Test the server and view coverage reports. Use of coverage reporting is recommended to indicate test suite completeness and to locate defunct code in the code base.
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

Queries can be made with the Postman Collection link ( https://www.getpostman.com/collections/a86a292798c7895425e2 )
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/0078de8f58d4ea0b78eb)

### Note For Windows Users

Python does not come by default for Windows users. Sometimes the PATH variable in Windows will point to the wrong path and you will have trouble running the `python` and `pipenv` commands. If you don't have Python installed then follow these steps. If the steps listed above did not work for you, try the following.

1. Clone the repo (`git clone https://github.com/codeforpdx/dwellinglybackend.git`)
2. Hit the Windows key on your keyboard and type `Microsoft Store`. Click on Microsoft store and search for Python. Download Python from the official Microsoft store. When you are installing **make sure you tick the Add to PATH checkbox [ ]** If you don't do this, it could result in you being unable to run the python or pip / pipenv commands.
3. Once Python is installed, run `pip3 install --user pipenv` If this command doesn't work, try running `python -m pip install --user pipenv`
4. Follow instructions 4-6 from the previous instructions section.

#### Still having issues on Windows?

If you are still having issues or if your command prompt is throwing an error that says `python is not a command` or `pip is not a command`, it is most likely a pathing issue where the ENV variable is pointing to the wrong directory. To try to troubleshoot, I suggest following this guide: ( https://github.com/LambdaSchool/CS-Wiki/wiki/Installing-Python-3-and-pipenv ).

### Mac-OS-Troubleshooting

Check to see where the Python you're running is located (`which python`). You should see something like `/Users/your_account_shortname/.pyenv/shims/python`.
If you don't see something similar, you may have several versions of Python installed elsewhere (via Anaconda or Homebrew). If (and only if) you'd like to clear out any previous homebrew-based installs, type `brew uninstall --ignore-dependencies python3 && brew uninstall --ignore-dependencies python`.

### Database migrations.

Database migrations are not used for development. Please ignore do not use migrations during development.  

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
