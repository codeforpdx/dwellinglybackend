Set up Dwelling Flask Testing Backend (for the first time)
NOTE: Database is SQLite3 via SQLAlchemy 

+ Github Repo: {https://github.com/codeforpdx/dwellinglybackend}
+ Live Server: {https://dwellinglyapi.herokuapp.com/ } 
+ Postman Collection: {https://www.postman.com/collections/a86a292798c7895425e2}

###To Start Server

1. Fork the backend and clone a copy ( https://help.github.com/en/github/getting-started-with-github/fork-a-repo )
2. Install Python ( https://realpython.com/installing-python/ )
3. Install virtualenv onto system (if not already installed)
    Mac + Linux: python3 -m venv env
    Windows: py -m venv env
4. Install dependencies while in main directory of dwellinglybackend forked copy
    pip3 install --no-cache-dir -r requirements.txt
5. Create virtual environment
    virtualenv env 
6. Activate the virtual environment 
    source env/bin/activate
7. Run the flask environment 
    pipenv run flask run 

Queries can be made with the Postman Collection link ( https://www.getpostman.com/collections/a86a292798c7895425e2 )

###This Backend Uses JWT for authorization 
Authorization header format:
Authorization Bearer JWT access token

###Enpoints

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

| method | route           | action                      |
| :----- | :-------------- | :-------------------------- |
| POST   | `/register/`    | Creates a new user          |
| GET    | `/users/`       | Gets all users (dev only)   |
| GET    | `/users/:uid`   | Gets a single user          |
| PATCH  | `/users/:uid`   | Updates a single user       |
| POST   | `/login     `   | Login a single user         |
| DELETE | `/users/:uid`   | Deletes a single user       |


```javascript
  {
        "username": "defaultUser",
        "password": "userPassword",
        "email": "user1@dwellingly.com",
        "archived": "false",
        "role": "admin"
        }
```

#### ENDPOINT: PROPERTIES

| method | route                | action                     |
| :----- | :------------------- | :------------------------- |
| POST   | `/properties/`       | Creates a new property     |
| GET    | `/properties/`       | Gets all properties        |
| GET    | `/properties/:id`    | Gets a single property     |
| PATCH  | `/properties/:id`    | Updates a single property  |
| PUT    | `/properties/:id`    | Archives a single property | not implemented yet
| DELETE | `/properties/:id`  | Deletes a single property  |


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
