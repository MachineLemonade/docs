---
title: "The Houston API Playground"
description: "Using the Graphql Playground."
date: 2018-10-12T00:00:00.000Z
slug: "houston-api"
---

## The Graphql Playground

The [houston-api](https://github.com/astronomer/houston-api) is the source of truth across the entire Astronomer Enterprise platform. Playground is a web portal which allows you to write graphql queries directly against the API.

If you are an **enterprise** customer, your playground will be located at https://houston.BASEDOMAIN/v1/

The Graphql playground allows you to directly interact with Astronomer API (Houston) via writing graphql queries. You can interact submit these queries through the playground, or directly to the Houston endpoint.

The [Graphql-playground Github](https://github.com/prisma/graphql-playground) contains more information on playground features.

## Querying Houston

### Authenticating

Each query requires proper authentication in the request headers. To authenticate, you can

- Get a temporary token from `app.BASEDOMAIN/token`
- Generate a Service Account key from the Astronomer UI.

Place the token with in `HTTP Headers` as `{"authorization": $TOKEN}`

(https://assets2.astronomer.io/main/docs/ee/headers.png)


#### Query Types

On Astronomer, you can ask for Graphql:

- [Query](https://graphql.org/learn/queries/#fields) - These return information
- [Mutatation](https://graphql.org/learn/queries/#mutations) - Queries to modify data
- [Subscriptions](https://graphql.org/blog/subscriptions-in-graphql-and-relay/) - Describes all of the events that can be subscribed to

### Schemas

Now that there is a valid auth token, you should be able to query all endpoints your user has access to. The [`Schema`](https://graphql.org/learn/schema/) tab on the right side shows how queries can be structured to get the information you need.

(https://assets2.astronomer.io/main/docs/ee/graphql_schema.png)


The query for `users` needs either an `email`, `username`, or a `UserUuid` as an input, and can return all of the fields under `Type Details`.

The below query, named `usersFullName`, can be used to return the `fullName` of a user:

```
query usersFullName {
  users(email:"viraj@astronomer.io")
  {
    username
    id
    fullName

  }
}
```

This returns the `username`, `id`, and `fullName` of the user with `viraj@astronomer.io` email. Results are shown on the `Resuls Viewer` on the right side of the page after hitting the Play Button.

(https://assets2.astronomer.io/main/docs/ee/query.gif)


#### Custom Types

Any datatype listed with `[]` in the `Schema` are compound datatypes and require additional fields to the query.
For example, adding the `email` field to the query above:

```
query users {
  users(email:"viraj@astronomer.io")
  {
    username
    id
    fullName
    emails
  }
}
```

This returns:

```
{
  "error": {
    "errors": [
      {
        "message": "Field \"emails\" of type \"[Email!]!\" must have a selection of subfields. Did you mean \"emails { ... }\"?",
        "locations": [
          {
            "line": 6,
            "column": 5
          }
        ],
        "extensions": {
          "code": "GRAPHQL_VALIDATION_FAILED"
        },
        "level": "ERROR",
        "timestamp": "2019-07-24T14:45:55"
      }
    ]
  }
}
```

The `emails` field requires additional subfields that can be found in the `Schema` tab.

(https://assets2.astronomer.io/main/docs/ee/users_custom_typeschema.png)


```
query users {
  users(email:"viraj@astronomer.io")
  {
    username
    id
    fullName
    emails
    {createdAt}

  }
}
```
By specifying a subfield of the `emails` type, the query executes successfully.

```
{
  "data": {
    "users": [
      {
        "username": "viraj@astronomer.io",
        "id": "cjx0ygnbf000t0a54ns8tmlum",
        "fullName": "Viraj Parekh",
        "emails": [
          {
            "createdAt": "2019-06-17T22:33:38.548Z"
          }
        ]
      }
    ]
  }
}
```
**Note:** Custom types are often composed of other custom types.

### Adding System Admins with a mutation
Mutations can be used to generate auth tokens, add system admins, and other things that `modify` the underlying database.

To add a system admin,

```
query users {
  users(email:"pete@astronomer.io")
  {
    id    

  }
}
```
Grab the returned `id` and feed it into the next mutation.

The `AddAdmin` query the mutation is named calls on the `createSystemRoleBinding`

```
mutation AddAdmin {
  createSystemRoleBinding(
    userId: $id
    role: SYSTEM_ADMIN
  ) {
    id
  }
}
```
