
How to set up Dwelling Flask Testing Backend. 
NOTE: no database setup here. Backend uses list-based live data 

# Setup Python on  your system
[Link to Guide](https://realpython.com/installing-python/ "Setup Python")
# Run 
virturalenv env 
# Run
source env/bin/activate
# Run
    pipenv run flask run 
# Run 
    pip install --no-cache-dir -r requirements.txt
# Run
    pipenv run flask run 

# Postman  Collection link
https://www.getpostman.com/collections/a86a292798c7895425e2


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
