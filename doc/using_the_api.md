## Using the API
### This Backend Uses JWT for authorization

A JWT token is required to authenticate requests. To get a token, use the login API:

```sh
curl http://127.0.0.1:5000/api/login \
--data "email=user1@dwellingly.org&password=1234"
```

Then, use the JWT token (`access_token`) as a Authorization bearer header:

```
curl http://127.0.0.1:5000/api/properties \
-H "Authorization: Bearer {put_token_here}"
```

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

### Endpoints

All endpoints are prefixed with `/api/`

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


#### ENDPOINT: PROPERTIES


| method | route                     | action                                  |
| :----- | :------------------------ | :-------------------------------------- |
| POST   | `/properties/`            | Creates a new property (admin only)     |
| GET    | `/properties/`            | Gets all properties                     |
| GET    | `/properties/:id`         | Gets a single property (admin only)     |
| PUT    | `/properties/:id`         | Updates a single property (admin only)  |
| DELETE | `/properties/:id`         | Deletes a single property (admin only)  |
| POST   | `/properties/archive/:id` | Archives a single property (admin only) |

```javascript
  {
    "id": 0,
    "name": "Garden Blocks",
    "address": "1654 NE 18th Ave.",
    "city": "Portland",
    "state": "OR",
    "zipCode": "97218",
    "num_units": 1,
    "leases": [serialized leases],
    "propertyManagers": [serialized property managers]
    "archived": False
  },
```

| method | route                     | action                                   |
| :----- | :------------------------ | :--------------------------------------- |
| PATCH  | `/properties/archive/`    | Archive multiple properties (admin only) |

```javascript
  {
    "ids": [id1, id2, id3]
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


#### ENDPOINT: StaffTenants

| method | route                        | action                                              |
| :----- | :--------------------------- | :-------------------------------------------------- |
| PATCH  | `/staff-tenants`             | Bulk action to update Staff/Tenant relationships    |

```javascript
	{
	staff: [<int:staff_id>, ...],
	tenants: [<int:tenant_id>, ...]
	}
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


#### ENDPOINT: TICKETS

| method | route              | action (all actions require user to be logged in)                 |
| :----- | :----------------- | :---------------------------------------------------------------- |
| POST   | `/tickets/`        | Creates a new ticket                                              |
| GET    | `/tickets/`        | Gets all tickets                                                  |
| DELETE | `/tickets/`        | Deletes tickets based on ticket ids listed in the request body's "ids" parameter      |
| GET    | `/tickets/:id`     | Gets a single ticket                                              |
| PUT    | `/tickets/:id`     | Updates a single ticket                                           |
| DELETE | `/tickets/:id`     | Deletes a single ticket                                           |

```javascript
    id: 1,
    issue: 'Property Damage',
    tenant: 'Renty McRenter',
    author_id: 1,
    tenant_id: 2,
    assignedUserID: 4,
    author: "user1 tester",
    status: "new",
    urgency: "Low",
    created_at: "07-01-2020 21:29:29",
    updated_at: "07-08-2020 22:20:29",
    minsPastUpdate: 745,
    assigned_staff: [{
        archived: false,
        created_at: "08/05/2021 02:52:30",
        email: "janice@joinpdx.org",
        firstName: "Janice",
        id: 10,
        lastActive: "08/05/2021 02:52:30",
        lastName: "Joinstaff",
        phone: "555-555-5555",
        role: 3,
        updated_at: "08/05/2021 02:52:30"
    }],
    notes: [
        {
            id: 2,
            ticketid: 1,
            created_at: "07-01-2020 21:29:29",
            text: "Tenant has over 40 cats.",
            user: "user2 tester"
        },
    ]
```

#### ENDPOINT: USER INVITE

| method | route           | action                 |
| :----- | :-------------- | :--------------------- |
| POST   | `/user/invite`  | Invite a user          |

```javascript
    'archived': False,
    'email': 'john51@gmail.com',
    'firstName': 'Amy',
    'lastName': 'Roberts',
    'password': 'xlLHBzv()3',
    'phone': '965-934-2320',
    'role': 3
```

##### Response (201)

```javascript
    {
        "message": "User Invited"
    }
```

#### ENDPOINT: WIDGETS

| method | route              | action (all actions require user to be logged in)   |
| :----- | :----------------- | :-------------------------------------------------- |
| GET    | `/widgets/`        | Pull down Widget Info                               |

```javascript
{
    "opentickets": {
        "new": {
            "allNew": {
                "stat": 7,
            },
            "unseen24Hrs": {
                "stat": 2,
            },
        },
        "inProgress": {
            "allInProgress": {
                "stat": 10,
            },
            "inProgress1Week": {
                "stat": 3,
            },
        },
    },
    "managers": [
        {
            "date": "Today",
            "firstName": "",
            "id": 1,
            "lastName": "Smith",
            "propertyName": ""
        },
    ],
}
```
