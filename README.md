Set up Dwelling Flask Testing Backend (for the first time)
NOTE: no database setup here. Backend uses list-based live data 

1. Fork the backend and clone a copy ( https://help.github.com/en/github/getting-started-with-github/fork-a-repo )
2. Install Python ( https://realpython.com/installing-python/ )
3. Install virtualenv onto system (if not already installed)
    Mac + Linux: python3 -m venv env
    Windows: py -m venv env
4. Install dependencies while in main directory of dwellinglybackend forked copy
    pip install --no-cache-dir -r requirements.txt
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

###Established Endpoints

#### ENDPOINT: USERS

| method | route           | action                 |
| :----- | :-------------- | :--------------------- |
| POST   | `v1/users/`     | Creates a new user     |
| GET    | `v1/users/`     | Gets all users         |
| GET    | `v1/users/:uid` | Gets a single user     |
| PATCH  | `v1/users/:uid` | Updates a single user  |
| PUT    | `v1/users/:uid` | Archives a single user |
| DELETE | `v1/users/:uid` | Deletes a single user  |


```javascript
  {
        "name": "Default User",
        "password": "userPassword",
        "username": "defaultUser",
        "email": "user1@dwellingly.com",
        "archived": "false",
        "uid": "user0",
        "phone":'555-555-5555',
        "role": {
                    "isAdmin": "true",
                    "isPropertyManager": "false",
                    "isStaff": "false"
                }
        }
```

#### ENDPOINT: PROPERTIES

| method | route                | action                     |
| :----- | :------------------- | :------------------------- |
| POST   | `v1/properties/`     | Creates a new property     |
| GET    | `v1/properties/`     | Gets all properties        |
| GET    | `v1/properties/:uid` | Gets a single property     |
| PATCH  | `v1/properties/:uid` | Updates a single property  |
| PUT    | `v1/properties/:uid` | Archives a single property |
| DELETE | `v1/properties/:uid` | Deletes a single property  |


```javascript
     {
    "id": "property1",
    "name": "Garden Blocks",
    "address": "1654 NE 18th Ave.",
    "zipCode": "97218",
    "city": "Portland",
    "state": "OR"
  },
```
