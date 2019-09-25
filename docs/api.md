# tahskr API

The tahskr API is a user based API in that once authenticated as a user, all methods will be limited to data owned by that user.

All dates and datetimes should be formatted to ISO 8601 standards.

## Methods

- [Create a User](#create-a-user)
- [Authenticate](#authenticate)
- [Create a To-Do List](#create-a-to-do-list)
- [Get All To-Do Lists](#get-all-to-do-lists)
- [Get a To-Do List](#get-a-to-do-list)
- [Update a To-Do List](#update-a-to-do-list)
- [Delete a To-Do List](#delete-a-to-do-list)
- [Create a To-Do](#create-a-to-do)
- [Get All To-Dos](#get-all-to-dos)
- [Get a To-Do](#get-a-to-do)
- [Update a To-Do](#update-a-to-do)
- [Delete a To-Do](#delete-a-to-do)

## Create a User

#### Method

POST

#### URL

/api/user

#### Headers

| Name         | Value            | Required? |
| ------------ | ---------------- | --------- |
| Content-Type | application/json | Yes       |

#### URL Parameters

None

#### Data Parameters

| Name         | Data Type | Required? | Details                        |
| ------------ | --------- | --------- | ------------------------------ |
| emailAddress | string    | Yes       | Must be a valid email address. |
| password     | string    | Yes       |                                |

#### Response Examples

![](https://img.shields.io/badge/201-Created-4DC292?style=flat-square)

```json
{
  "created": "2019-09-25T13:13:14.702375",
  "emailAddress": "john@example.com",
  "id": 243
}
```

![](https://img.shields.io/badge/400-Client%20Error-DC555C?style=flat-square)

```json
{
  "message": {
    "emailAddress": ["Not a valid email address."]
  }
}
```

## Authenticate

Authenticate a username and password to retrieve an authentication token.

#### Method

POST

#### URL

/auth

#### Headers

| Name         | Value            | Required? |
| ------------ | ---------------- | --------- |
| Content-Type | application/json | Yes       |

#### URL Parameters

None

#### Data Parameters

#### Data Parameters

| Name         | Data Type | Required? | Details |
| ------------ | --------- | --------- | ------- |
| emailAddress | string    | Yes       |         |
| password     | string    | Yes       |         |

#### Responses Examples

![](https://img.shields.io/badge/200-OK-4DC292?style=flat-square)

```json
{
  "created": "2019-09-25T13:17:34.742383",
  "expiry": "2019-10-25T13:17:34.742383",
  "lastUsed": "2019-09-25T13:17:34.742383",
  "token": "f1737df5-65f3-48dh-8665-3074d112de39",
  "userId": 243
}
```

![](https://img.shields.io/badge/400-Client%20Error-DC555C?style=flat-square)

```json
{
  "message": {
    "emailAddress": ["Missing data for required field."]
  }
}
```

![](https://img.shields.io/badge/401-Unauthorised-DC555C?style=flat-square)

```json
{
  "message": "Invalid email address or password."
}
```

## Create a To-Do List

#### Method

POST

#### URL

/api/todolist

#### Headers

| Name         | Value                                                      | Required? |
| ------------ | ---------------------------------------------------------- | --------- |
| token        | An authentication token retrieved using the /auth service. | Yes       |
| Content-Type | application/json                                           | Yes       |

#### URL Parameters

None

#### Data Parameters

| Name | Data Type | Required? | Details |
| ---- | --------- | --------- | ------- |
| name | string    | Yes       |         |

#### Responses Examples

![](https://img.shields.io/badge/201-Created-4DC292?style=flat-square)

```json
{
  "created": "2019-09-25T13:20:56.676620",
  "id": 567,
  "name": "Personal",
  "userId": 243
}
```

![](https://img.shields.io/badge/400-Client%20Error-DC555C?style=flat-square)

```json
{
  "message": {
    "name": ["Field may not be null."]
  }
}
```

![](https://img.shields.io/badge/401-Unauthorised-DC555C?style=flat-square)

```json
{
  "message": "Authentication token invalid."
}
```

## Get All To-Do Lists

#### Method

GET

#### URL

/api/todolist

#### Headers

| Name  | Value                                                      | Required? |
| ----- | ---------------------------------------------------------- | --------- |
| token | An authentication token retrieved using the /auth service. | Yes       |

#### URL Parameters

None

#### Data Parameters

None

#### Responses Examples

![](https://img.shields.io/badge/200-OK-4DC292?style=flat-square)

```json
[
  {
    "created": "2019-09-25T13:20:52.966185",
    "id": 567,
    "name": "Personal",
    "userId": 243
  },
  {
    "created": "2019-09-25T13:20:56.676620",
    "id": 598,
    "name": "Work",
    "userId": 243
  }
]
```

![](https://img.shields.io/badge/401-Unauthorised-DC555C?style=flat-square)

```json
{
  "message": "Authentication token invalid."
}
```

## Get a To-Do List

#### Method

GET

#### URL

/api/todolist/<id>

#### Headers

| Name  | Value                                                      | Required? |
| ----- | ---------------------------------------------------------- | --------- |
| token | An authentication token retrieved using the /auth service. | Yes       |

#### URL Parameters

None

#### Data Parameters

None

#### Responses Examples

![](https://img.shields.io/badge/200-OK-4DC292?style=flat-square)

```json
{
  "created": "2019-09-25T13:20:56.676620",
  "id": 567,
  "name": "Personal",
  "userId": 243
}
```

![](https://img.shields.io/badge/401-Unauthorised-DC555C?style=flat-square)

```json
{
  "message": "Authentication token invalid."
}
```

![](https://img.shields.io/badge/404-Not%20Found-DC555C?style=flat-square)

```json
{
  "message": "The requested resource was not found."
}
```

## Update a To-Do List

#### Method

PATCH

#### URL

/api/todolist/<id>

#### Headers

| Name         | Value                                                      | Required? |
| ------------ | ---------------------------------------------------------- | --------- |
| token        | An authentication token retrieved using the /auth service. | Yes       |
| Content-Type | application/json                                           | Yes       |

#### URL Parameters

None

#### Data Parameters

| Name | Data Type | Required? | Details |
| ---- | --------- | --------- | ------- |
| name | String    | Yes       |         |

#### Responses Examples

![](https://img.shields.io/badge/200-OK-4DC292?style=flat-square)

```json
{
  "created": "2019-09-25T13:20:56.676620",
  "id": 567,
  "name": "Home",
  "userId": 243
}
```

![](https://img.shields.io/badge/400-Client%20Error-DC555C?style=flat-square)

```json
{
  "message": {
    "name": ["Field may not be null."]
  }
}
```

![](https://img.shields.io/badge/401-Unauthorised-DC555C?style=flat-square)

```json
{
  "message": "Authentication token invalid."
}
```

![](https://img.shields.io/badge/404-Not%20Found-DC555C?style=flat-square)

```json
{
  "message": "The requested resource was not found."
}
```

## Delete a To-Do List

#### Method

DELETE

#### URL

/api/todolist/<id>

#### Headers

| Name  | Value                                                      | Required? |
| ----- | ---------------------------------------------------------- | --------- |
| token | An authentication token retrieved using the /auth service. | Yes       |

#### URL Parameters

None

#### Data Parameters

None

#### Responses Examples

![](https://img.shields.io/badge/200-OK-4DC292?style=flat-square)

```json
{
  "message": "Deletion successful."
}
```

![](https://img.shields.io/badge/401-Unauthorised-DC555C?style=flat-square)

```json
{
  "message": "Authentication token invalid."
}
```

![](https://img.shields.io/badge/404-Not%20Found-DC555C?style=flat-square)

```json
{
  "message": "The requested resource was not found."
}
```

## Create a To-Do

#### Method

POST

#### URL

/api/todo

#### Headers

| Name         | Value                                                      | Required? |
| ------------ | ---------------------------------------------------------- | --------- |
| token        | An authentication token retrieved using the /auth service. | Yes       |
| Content-Type | application/json                                           | Yes       |

#### URL Parameters

None

#### Data Parameters

| Name              | Data Type | Required? | Details                                 |
| ----------------- | --------- | --------- | --------------------------------------- |
| summary           | string    | Yes       |                                         |
| parentId          | int       | No        | Set to create a sub-task of the parent. |
| listId            | int       | No        | A To-Do List id.                        |
| notes             | string    | No        |                                         |
| important         | boolean   | No        | Defaults to false.                      |
| snoozeDate        | string    | No        |                                         |
| completedDatetime | string    | No        |                                         |

#### Responses Examples

![](https://img.shields.io/badge/201-Created-4DC292?style=flat-square)

```json
{
  "completedDatetime": null,
  "created": "2019-09-25T20:10:35.943554",
  "id": 2,
  "important": false,
  "listId": null,
  "notes": null,
  "parentId": null,
  "snoozeDate": null,
  "summary": "My First To Do",
  "userId": 243
}
```

![](https://img.shields.io/badge/400-Client%20Error-DC555C?style=flat-square)

```json
{
  "message": {
    "important": ["Not a valid boolean."]
  }
}
```

![](https://img.shields.io/badge/401-Unauthorised-DC555C?style=flat-square)

```json
{
  "message": "Authentication token invalid."
}
```

## Get All To-Dos

#### Method

GET

#### URL

/api/todo

#### Headers

| Name  | Value                                                      | Required? |
| ----- | ---------------------------------------------------------- | --------- |
| token | An authentication token retrieved using the /auth service. | Yes       |

#### URL Parameters

| Name           | Required? | Details                                                                                    |
| -------------- | --------- | ------------------------------------------------------------------------------------------ |
| parentId       | No        | Return sub-tasks of this To-Do. Defaults to null.                                          |
| completed      | No        | null (default) = Return all. true = Return only completed. false = Return only incomplete. |
| excludeSnoozed | No        | If true, exclude To-Dos with a snoozedDate in the future. Defaults to false.               |

#### Data Parameters

None

#### Responses Examples

![](https://img.shields.io/badge/200-OK-4DC292?style=flat-square)

```json
[
  {
    "completedDatetime": null,
    "created": "2019-09-25T20:10:35.943554",
    "id": 1345,
    "important": false,
    "listId": null,
    "notes": null,
    "parentId": null,
    "snoozeDate": null,
    "summary": "My First To Do",
    "userId": 243
  },
  {
    "completedDatetime": null,
    "created": "2019-09-25T20:10:36.643565",
    "id": 1367,
    "important": true,
    "listId": null,
    "notes": "Think of better dummy data.",
    "parentId": null,
    "snoozeDate": "2019-09-26",
    "summary": "Another To Do",
    "userId": 243
  }
]
```

![](https://img.shields.io/badge/400-Client%20Error-DC555C?style=flat-square)

```json
{
  "message": {
    "parentId": ["Not a valid integer."]
  }
}
```

![](https://img.shields.io/badge/401-Unauthorised-DC555C?style=flat-square)

```json
{
  "message": "Authentication token invalid."
}
```

## Get a To-Do

#### Method

GET

#### URL

/api/todo/<id>

#### Headers

| Name  | Value                                                      | Required? |
| ----- | ---------------------------------------------------------- | --------- |
| token | An authentication token retrieved using the /auth service. | Yes       |

#### URL Parameters

None

#### Data Parameters

None

#### Responses Examples

![](https://img.shields.io/badge/200-OK-4DC292?style=flat-square)

```json
{
  "completedDatetime": null,
  "created": "2019-09-25T20:10:35.943554",
  "id": 1345,
  "important": false,
  "listId": null,
  "notes": null,
  "parentId": null,
  "snoozeDate": null,
  "summary": "My First To Do",
  "userId": 243
}
```

![](https://img.shields.io/badge/401-Unauthorised-DC555C?style=flat-square)

```json
{
  "message": "Authentication token invalid."
}
```

![](https://img.shields.io/badge/404-Not%20Found-DC555C?style=flat-square)

```json
{
  "message": "The requested resource was not found."
}
```

## Update a To-Do

#### Method

PATCH

#### URL

/api/todo/<id>

#### Headers

| Name         | Value                                                      | Required? |
| ------------ | ---------------------------------------------------------- | --------- |
| token        | An authentication token retrieved using the /auth service. | Yes       |
| Content-Type | application/json                                           | Yes       |

#### URL Parameters

None

#### Data Parameters

| Name              | Data Type | Required? | Details                                 |
| ----------------- | --------- | --------- | --------------------------------------- |
| summary           | string    | No        | Cannot be null.                         |
| parentId          | int       | No        | Set to create a sub-task of the parent. |
| listId            | int       | No        | A To-Do List id.                        |
| notes             | string    | No        |                                         |
| important         | boolean   | No        |                                         |
| snoozeDate        | string    | No        |                                         |
| completedDatetime | string    | No        |                                         |

#### Responses Examples

![](https://img.shields.io/badge/200-OK-4DC292?style=flat-square)

```json
{
  "completedDatetime": null,
  "created": "2019-09-25T20:10:35.943554",
  "id": 1345,
  "important": true,
  "listId": null,
  "notes": null,
  "parentId": null,
  "snoozeDate": null,
  "summary": "My First To Do - Updated",
  "userId": 243
}
```

![](https://img.shields.io/badge/400-Client%20Error-DC555C?style=flat-square)

```json
{
  "message": {
    "summary": ["Field may not be null."]
  }
}
```

![](https://img.shields.io/badge/401-Unauthorised-DC555C?style=flat-square)

```json
{
  "message": "Authentication token invalid."
}
```

![](https://img.shields.io/badge/404-Not%20Found-DC555C?style=flat-square)

```json
{
  "message": "The requested resource was not found."
}
```

## Delete a To-Do

#### Method

DELETE

#### URL

/api/todo/<id>

#### Headers

None

#### URL Parameters

None

#### Data Parameters

None

#### Responses Examples

![](https://img.shields.io/badge/200-OK-4DC292?style=flat-square)

```json
{
  "message": "Deletion successful."
}
```

![](https://img.shields.io/badge/401-Unauthorised-DC555C?style=flat-square)

```json
{
  "message": "Authentication token invalid."
}
```

![](https://img.shields.io/badge/404-Not%20Found-DC555C?style=flat-square)

```json
{
  "message": "The requested resource was not found."
}
```
