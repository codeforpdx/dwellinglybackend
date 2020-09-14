## Installation
Set up Dwelling Flask Testing Backend (for the first time)
NOTE: Database is SQLite3 via SQLAlchemy

[Note for Windows users](#Note-For-Windows-Users)

[Note for Mac users](#Mac-OS-Alternative-Setup-Instructions-(for-those-who-have-never-used-Python/having-path-errors))


**Note about Python Versions**: You may have to substitue **python** with **python3** and **pip** with **pip3** in the instructions below.


1. Clone the repo (`git clone https://github.com/codeforpdx/dwellinglybackend.git`)
2. Install Python ( https://realpython.com/installing-python/ )
3. Install [pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today)
4. Install dependencies `pipenv install -d`
   - If you get the error `ImportError: cannot import name 'Feature' from 'setuptools'`, your setuptools version might be at 46 or later. You may be able to get it to work using version 45 (e.g. `pip3 install setuptools==45`) 
5. Create and Seed the database
   - Run: `pipenv run python manage.py create`
   - To re-seed the database from scratch, delete data.db before running the script
   - Look for the file data.db to be created in the root directory
   - If you get the error `ImportError: No module named flask` or similar, you may need to run `pipenv shell` to launch virtual environment.
6. Start the server using the flask environment (required every time the project is re-opened):
   - Run: `pipenv run flask run`
   - Run + restart the server on changes: `pipenv run flask run --reload`

6. Test the server and view coverage reports. Use of coverage reporting is recommended to indicate test suite completeness and to locate defunct code in the code base.
    - Run the tests: `pipenv run pytest --cov .`
      - View coverage for a particular directory: `pipenv run pytest --cov [directory]`
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

### Mac OS Alternative Setup Instructions (for those who have never used Python/having path errors)

1. Clone the repo (`git clone https://github.com/codeforpdx/dwellinglybackend.git`)
2. Install Python ( https://realpython.com/installing-python/ )
3. Install pipenv: `pip3 install --user pipenv`
4. Shell into the environment configured by your Pipfile `pipenv shell`
  - This brings you into a partitioned environment set up to spec with your Pipfile. Often people who skip this step will have path and version errors.
5. Run: `pipenv run python manage.py create`
6. Run: `pipenv run flask run`
7. Login using one of the accounts below and you should be good to go!


### Database commands. 
- Create and Seed the Database: `pipenv run python manage.py create`
- Delete, create, Seed the Database: `pipenv run python manage.py recreate`
- Delete the Database: `pipenv run python manage.py drop`


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

