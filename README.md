*Looking for the [Dwellingly App front end?](https://github.com/codeforpdx/dwellingly-app)*

## Dwellingly App Backend

Set up Dwelling Flask Testing Backend (for the first time)
NOTE: Database is SQLite3 via SQLAlchemy

+ Github Repo: { https://github.com/codeforpdx/dwellinglybackend }
+ Live Server: {https://dwellinglyapi.herokuapp.com/}

### To Start Server

1. Clone the repo (`git clone https://github.com/codeforpdx/dwellinglybackend.git`)
2. Install Python ( https://realpython.com/installing-python/ )
3. Install pipenv: `pip3 install --user pipenv`
4. Seed the database
    - Run: `python seed_db.py`
      - To re-seed the database from scratch, delete data.db before running the script
    - Look for the file data.db to be created in the root directory

5. Start the server using the flask environment (required every time the project is re-opened):
    - Run: `pipenv run flask run`
    - Run + restart the server on changes:  `pipenv run flask run --reload`

Queries can be made with the Postman Collection link ( https://www.getpostman.com/collections/a86a292798c7895425e2 )


## Alternative Setup Instructions (for those who have never used Python/having path errors)

1. Clone the repo (`git clone https://github.com/codeforpdx/dwellinglybackend.git`)
2. Install Python ( https://realpython.com/installing-python/ )
3. Install pipenv: `pip3 install --user pipenv`
4. Shell into the environment configured by your Pipfile `pipenv shell`
  - This brings you into a partitioned environment set up to spec with your Pipfile. Often people who skip this step will have path and version errors.
5. Run: `python seed_db.py`
6. Run: `pipenv run flask run`
7. Login using one of the accounts below and you should be good to go!

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

| method | route                  | action                               |
| :----- | :--------------------- | :----------------------------------- |
| POST   | `/register/`           | Creates a new user                   |
| GET    | `/users/`              | Gets all users (dev only)            |
| GET    | `/users/:uid`          | Gets a single user (admin only)      |  
| PATCH  | `/users/:uid`          | Updates a single user                |  not implemented yet
| POST   | `/login     `          | Login a single user                  |
| POST   | `/user/archive/:uid`   | Archives a single user (admin only)  |
| DELETE | `/users/:uid`          | Deletes a single user (admin only)   |


### This Backend Uses JWT for authorization

Authorization header format:
```javascript
Authorization Bearer < JWT access token >
```

### The database is seeded with 3 default users

```javascript
    [{
        "email": "user1@dwellingly.org",
        "password": "1234",
        "firstName": "user1",
        "lastName": "tester",
        "archived": "false",
        "role": "admin"
    },
    {
        "email": "user2@dwellingly.org",
        "password": "1234",
        "firstName": "user2",
        "lastName": "tester",
        "archived": "false",
        "role": "admin"
    },
    {
        "email": "user3@dwellingly.org",
        "password": "1234",
        "firstName": "user3",
        "lastName": "tester",
        "archived": "false",
        "role": "admin"
    }]
```


#### ENDPOINT: PROPERTIES

| method | route                        | action                                   |
| :----- | :--------------------------- | :--------------------------------------- |
| POST   | `/properties/`               | Creates a new property (admin only)      |
| GET    | `/properties/`               | Gets all properties                      |
| GET    | `/properties/:id`            | Gets a single property (admin only)      |
| PATCH  | `/properties/:id`            | Updates a single property                | not implemented
| PUT    | `/properties/:id`            | Updates a single property (admin only)   |
| DELETE | `/properties/:id`            | Deletes a single property (admin only)   |
| POST   | `/properties/archive/:id`    | Archives a single property (admin only)  |


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

#### ENDPOINT: TENANTS

| method | route                        | action                                   |
| :----- | :--------------------------- | :--------------------------------------- |
| POST   | `/tenants/`                  | Creates a new tenant (admin only)        |
| GET    | `/tenants/`                  | Gets all tenants                         |
| GET    | `/tenants/:id`               | Gets a single tenant (admin only)      |
| PUT    | `/tenants/:id`               | Updates a single tenant (admin only)   |
| DELETE | `/tenants/:id`               | Deletes a single tenant (admin only)   |

```javascript
    {
        "id": 1,
        "firstName": "Renty",
        "lastName": "McRenter",
        "phone": "800-RENT-ALOT",
        "propertyID": 1,
        "staffIDs": [1, 2]
    },
```

#### ENDPOINT: EMERGENCY NUMBERS

| method | route                        | action                                              |
| :----- | :--------------------------- | :-------------------------------------------------- |
| POST   | `/emergencycontacts/`        | Creates a new emergency contact (admin only)        |
| GET    | `/emergencycontacts/`        | Gets all emergency contacts                         |
| GET    | `/emergencycontacts/:id`     | Gets a single emergency contact (admin only)        |
| PUT    | `/emergencycontacts/:id`     | Updates a single emergency contact (admin only)     |
| DELETE | `/emergencycontacts/:id`     | Deletes a single emergency contact (admin only)     |

```javascript
    {
        "id": 1,
        "name": "Narcotics Anonymous",
        "description": "Addiction services")
        "contact_numbers": [
            {
                "number": "503-345-9839"
            },
            {
                "number": "503-291-9111",
                "numtype": "Phone",
                "extension": "x123"
            }
        ]
    }
```

#### ENDPOINT: EMAIL

| method | route                | action                     |
| :----- | :------------------- | :------------------------- |
| POST   | `/user/message`      | Send Message to a user     |


#### Example Request
```javascript
     {
    "userid": 1,
    "title": "Test email title",
    "body": "Dwellingly Test email body"
  },
