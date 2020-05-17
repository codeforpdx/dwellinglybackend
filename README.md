_Looking for the [Dwellingly App front end?](https://github.com/codeforpdx/dwellingly-app)_

## Dwellingly App Backend

Set up Dwelling Flask Testing Backend (for the first time)
NOTE: Database is SQLite3 via SQLAlchemy

- Github Repo: { https://github.com/codeforpdx/dwellinglybackend }
- Live Server: {https://dwellinglyapi.herokuapp.com/}

### To Start Server

1. Clone the repo (`git clone https://github.com/codeforpdx/dwellinglybackend.git`)
2. Install Python ( https://realpython.com/installing-python/ )
3. Install pipenv: `pip3 install --user pipenv`
4. Seed the database

   - Run: `python seed_db.py`
     - To re-seed the database from scratch, delete data.db before running the script
   - Look for the file data.db to be created in the root directory

5. Run `pipenv install`
6. Start the server using the flask environment (required every time the project is re-opened):
   - Run: `pipenv run flask run`
   - Run + restart the server on changes: `pipenv run flask run --reload`

Queries can be made with the Postman Collection link ( https://www.getpostman.com/collections/a86a292798c7895425e2 )

### Note For Windows Users

Python does not come by default for Windows users. Sometimes the PATH variable in Windows will point to the wrong path and you will have trouble running the `python` and `pipenv` commands. If you don't have Python installed then follow these steps. If the steps listed above did not work for you, try the following.

1. Clone the repo (`git clone https://github.com/codeforpdx/dwellinglybackend.git`)
2. Hit the Windows key on your keyboard and type `Microsoft Store`. Click on Microsoft store and search for Python. Download Python from the official Microsoft store. When you are installing **make sure you tick the Add to PATH checkbox [ ]** If you don't do this, it could result in you being unable to run the python or pip / pipenv commands.
3. Once Python is installed, run `pip3 install --user pipenv` If this command doesn't work, try running `python -m pip install --user pipenv`
4. Follow instructions 4-6 from the previous instructions section.

#### Still having issues on Windows?

If you are still having issues or if your command prompt is throwing an error that says `python is not a command` or `pip is not a command`, it is most likely a pathing issue where the ENV variable is pointing to the wrong directory. To try to troubleshoot, I suggest following this guide: ( https://github.com/LambdaSchool/CS-Wiki/wiki/Installing-Python-3-and-pipenv ).

### Endpoints

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

go to

#### ENDPOINT: USER Model

| method | route                | action                              |
| :----- | :------------------- | :---------------------------------- |
| POST   | `/register/`         | Creates a new user                  |
| GET    | `/users/`            | Gets all users (dev only)           |
| GET    | `/users/:uid`        | Gets a single user (admin only)     |
| PATCH  | `/users/:uid`        | Updates a single user               | not implemented yet |
| POST   | `/login`             | Login a single user                 |
| POST   | `/user/archive/:uid` | Archives a single user (admin only) |
| DELETE | `/users/:uid`        | Deletes a single user (admin only)  |

### This Backend Uses JWT for authorization

Authorization header format:

```javascript
Authorization Bearer < JWT access token >
```

### The database is seeded with 3 default users

```javascript
[
	{
		email: "user1@dwellingly.org",
		password: "1234",
		firstName: "user1",
		lastName: "tester",
		archived: "false",
		role: "admin",
	},
	{
		email: "user2@dwellingly.org",
		password: "1234",
		firstName: "user2",
		lastName: "tester",
		archived: "false",
		role: "admin",
	},
	{
		email: "user3@dwellingly.org",
		password: "1234",
		firstName: "user3",
		lastName: "tester",
		archived: "false",
		role: "admin",
	},
];
```

#### ENDPOINT: PROPERTIES

| method | route                     | action                                  |
| :----- | :------------------------ | :-------------------------------------- |
| POST   | `/properties/`            | Creates a new property (admin only)     |
| GET    | `/properties/`            | Gets all properties                     |
| GET    | `/properties/:id`         | Gets a single property (admin only)     |
| PATCH  | `/properties/:id`         | Updates a single property               | not implemented |
| PUT    | `/properties/:id`         | Updates a single property (admin only)  |
| DELETE | `/properties/:id`         | Deletes a single property (admin only)  |
| POST   | `/properties/archive/:id` | Archives a single property (admin only) |

```javascript
     {
    "id": "property1",
    "name": "Garden Blocks",
    "address": "1654 NE 18th Ave.",
    "zipCode": "97218",
    "city": "Portland",
    "state": "OR",
    "archived": False
  },
```

#### ENDPOINT: EMAIL

| method | route           | action                 |
| :----- | :-------------- | :--------------------- |
| POST   | `/user/message` | Send Message to a user |

#### Example Request

```javascript
     {
    "userid": 1,
    "title": "Test email title",
    "body": "Dwellingly Test email body"
  },
```
