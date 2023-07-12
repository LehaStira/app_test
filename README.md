# Test project in flask for managing users

## Register User

- **URL:** `/register`
- **Type of request:** POST
- **Needed token:** No
- **Body of request:**

```json
{
    "username": "TestSecondUser",
    "email": "test_second@gmail.com",
    "password": "123412341"
}
```
- **Answer:**

```json
{
    "created_on": "2023-07-12 16:04:06",
    "email": "test_second@gmail.com",
    "last_login": "2023-07-12 16:04:06",
    "user_id": 1,
    "username": "TestSecondUser"
}
```

## Login User

- **URL:** `/login`
- **Type of request:** POST
- **Needed token:** No
- **Body of request:**

```json
{
    "username": "TestSecondUser",
    "email": "test_second@gmail.com",
    "password": "123412341"
}
```
- **Answer:**

```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOjEsImV4cCI6MTY4OTE3OTY5MX0.EQ6JriaBw2JgJrqFPiCCai22vcvpEBBlHM0TcBY3kdI"
}
```


## Update user by id

- **URL:** `/users/<id>`
- **Type of request:** PUT
- **Needed token:** Yes
- **Body of request:**

```json
{
    "username": "TestSecond11111User",
    "email": "te111st_second@gmail.com",
    "password": "123412341"
}
```
- **Answer:**

```json
{
{
    "created_on": "2023-07-12 15:48:31",
    "email": "te111st_second@gmail.com",
    "last_login": "2023-07-12 15:48:31",
    "user_id": 2,
    "username": "TestSecond11111User"
}
}
```


## Delete user by id

- **URL:** `/users/<id>`
- **Type of request:** DELETE
- **Needed token:** Yes
- **Answer:**

```json
{
    "message": "User with user_id = 2 was successfully deleted"
}
```

## Get all users

- **URL:** `/users`
- **Type of request:** GET
- **Needed token:** No
- **Answer:**

```json
[
    {
        "created_on": "2023-07-12 15:48:03",
        "email": "test_first@gmail.com",
        "last_login": "2023-07-12 15:48:03",
        "user_id": 1,
        "username": "TestFirstUser"
    },
    {
        "created_on": "2023-07-12 15:48:31",
        "email": "test_second@gmail.com",
        "last_login": "2023-07-12 15:48:31",
        "user_id": 2,
        "username": "TestSecondUser"
    }
]
```
## Get user by id

- **URL:** `/users/<id>`
- **Type of request:** GET
- **Needed token:** No
- **Answer:**

```json
{
    "created_on": "2023-07-12 15:48:31",
    "email": "test_second@gmail.com",
    "last_login": "2023-07-12 15:48:31",
    "user_id": 2,
    "username": "TestSecondUser"
}
```



