## APIs

### /api/tmobile/bills

Get all the bills

```json
[
  {
    "month": "202001",
    "total": 232.0
  },
  {
    "month": "202002",
    "total": 232.0
  },
  
  {
    "month": "202003",
    "total": 232.0
  }
]
```

### /api/tmobile/bills/202001

Gets the bill details for given month

```json
{
  "month": "202002",
  "total": 232.0,
  "planAmount": 19.00,
  "bill":
  {
      "number": "503 444 1234",
      "total": 23.00,
      "services": 1.0,
      "equipment": 2.0
  }
}
```

### /api/tmobile/users

Gets all the users info

```json
[
  {
    "primary": "primary1",
    "users": [
      {
        "name": "user1",
        "phone": "503 111 1111"
      },
      {
        "name": "user2",
        "phone": "503 222 2222"
      },
      {
        "name": "user3",
        "phone": "503 333 3333"
      }
    ]
  },
  {
    "primary": "primary2",
    "users": [
      {
        "name": "user4",
        "phone": "503 444 4444"
      },
      {
        "name": "user5",
        "phone": "503 555 5555"
      },
      {
        "name": "user6",
        "phone": "503 666 6666"
      }
    ]
  }
]
```
## UI
Month  - Total
   - Details
        Name   Total  Equipment   Services   OneTime
By Primary
   2020-01
        Name   Total  Equipment   Services   OneTime

## Dynamo db
|  Primary Key   |  Sort Key |     Attributes  |
|----------------|-----------  |-----------------|
|  Bill202101    |           |  Total
|                |  Summary  |  230.00
|                |           |    Service    Eqiupment    OneTime    Total  
|                |  Number#123  |
|                |  Phone-3  |
|  Bill202102    |  Phone-1  |
|                |  Phone-2  |
|                |  Phone-3  |
|  Users         |  Primay1  |   Users
|                |  Name1    |   User1,User2,User3
|                |  Name2    |   User3,User4,User5
|  PhoneNames    |  Name     |   Phone           
|                |  User1    |   503 123 4567
|                |  User2    |   503 444 1111

Query:  
    By Month( primary key)
    Users
    NameToPhone

## Dev locally
* sam build
* run dynamodb docker
```cmd
docker run -p 8000:8000 amazon/dynamodb-local
```
* Invoking lambda function
```cmd
sam local invoke "TMobileFunction" -e event.json
```


## Resources
[Dynamo DB Queries](https://www.fernandomc.com/posts/ten-examples-of-getting-data-from-dynamodb-with-python-and-boto3/)
[Sort Keys](https://aws.amazon.com/blogs/database/using-sort-keys-to-organize-data-in-amazon-dynamodb/#:~:text=Each%20item%20in%20a%20DynamoDB,be%20unique%20across%20the%20table.)
[Dynamo DB Key Concepts](https://www.dynamodbguide.com/key-concepts/)