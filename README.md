Set up Dwelling Flask Testing Backend (for the first time)
NOTE: Database is SQLite3 via SQLAlchemy 

+ Github Repo: {https://github.com/codeforpdx/dwellinglybackend}
+ Live Server: {https://dwellinglyapi.herokuapp.com/ } 

### To Start Server

1. Clone the repo (`git clone https://github.com/codeforpdx/dwellinglybackend.git`)
2. Install Python ( https://realpython.com/installing-python/ )
3. Install virtualenv onto system (if not already installed)

    - Mac + Linux: `python3 -m venv env`
    - Windows: `python -m venv env`

4. Install dependencies while in main directory of dwellinglybackend forked copy

    - `pip3 install --no-cache-dir -r requirements.txt`

5. Create virtual environment: 

    - `virtualenv env`
    - To install virtualenv: `pip3 install --user virtualenv`

6. Activate the virtual environment 

    - Mac + Linux: `source env/bin/activate`
    - Windows: `source env/Scripts/activate`
    
7. Start the server using the flask environment (required every time the project is re-opened):

    - Run: `pipenv run flask run`
    - Run + restart the server on changes:  `pipenv run flask run --reload`
    - To install pipenv: `pip3 install --user pipenv`

Queries can be made with the Postman Collection link ( https://www.getpostman.com/collections/a86a292798c7895425e2 )

###Endpoints

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


###This Backend Uses JWT for authorization 

Authorization header format:
```javascript
Authorization Bearer < JWT access token >
```

###The database is seeded with 3 default users

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
