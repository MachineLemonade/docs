---
title: "The Houston API Playground"
description: "Using The GraphQL Playground."
date: 2018-10-12T00:00:00.000Z
slug: "houston-api"
---

## The GraphQL Playground

The [houston-api](https://github.com/astronomer/houston-api) is the source of truth across the entire Astronomer Enterprise platform. Playground is a web portal which allows you to write GraphQL queries directly against the API.You can interact submit these queries through the playground, or directly to the Houston endpoint.

If you are an **enterprise** customer, your playground will be located at https://houston.BASEDOMAIN/v1/

The [GraphQL-playground Github](https://github.com/prisma/GraphQL-playground) contains more information on playground features.

## Querying Houston
To start off, head to https://houston.BASEDOMAIN/v1/

### Authenticating

Each query requires proper authentication in the request headers. To authenticate, you can

- Get a temporary token from `app.BASEDOMAIN/token`
- Generate a Service Account key from the Astronomer UI.

Expand the `HTTP Headers` on the bottom left and include the token formatted as: `{"authorization": $TOKEN}`

![Headers](https://assets2.astronomer.io/main/docs/ee/headers.png)


#### Query Types

On Astronomer, you can ask for GraphQL:

- [Queries](https://GraphQL.org/learn/queries/#fields) - Queries to return information
- [Mutations](https://GraphQL.org/learn/queries/#mutations) - Queries to modify data
- [Subscriptions](https://GraphQL.org/blog/subscriptions-in-GraphQL-and-relay/) - Describes all of the events that can be subscribed to

This guide will stay away from Subscriptions.

### Schemas and Sample Query

With a valid token in the HTTP headers, you should be able to query all endpoints your user has access to. The [`Schema`](https://GraphQL.org/learn/schema/) tab on the right side shows how queries can be structured to get the information you need.

![Schema](https://assets2.astronomer.io/main/docs/ee/GraphQL_schema.png)

The query for `deployment` needs either an `workspaceUuid`, `deploymentUuid`, or a `releaseName` as an input, and can return all of the fields under `Type Details`.

The below query, named `deploymentinfo`, can be used to return the `config` of a deployment:

```
query deploymentinfo {
  deployments(releaseName:"astral-perturbation-4616")
  {
    id
    config

  }
}
```
Results are shown on the `Resuls Viewer` on the right side of the page after hitting the Play Button.

![Query](https://assets2.astronomer.io/main/docs/ee/deployment_query.gif)


#### Custom Types

Any datatype listed with `[]` in the `Schema` requires additional fields to the query.
For example, adding the `urls` field to the query above:

```
query deploymentinfo {
  deployments(releaseName:"astral-perturbation-4616")
  {
    id
    config
    urls

  }
}
```

This returns:

```
{
  "error": {
    "errors": [
      {
        "message": "Field \"urls\" of type \"[DeploymentUrl]\" must have a selection of subfields. Did you mean \"urls { ... }\"?",
        "locations": [
          {
            "line": 5,
            "column": 5
          }
        ],
        "extensions": {
          "code": "GraphQL_VALIDATION_FAILED"
        },
        "level": "ERROR",
        "timestamp": "2019-07-24T16:52:33"
      }
    ]
  }
}
```

The `urls` field requires additional subfields that can be found in the `Schema` tab.

![Custom Type](https://assets2.astronomer.io/main/docs/ee/deployments_custom_typeschema.png)


```
query deployment {
  deployments(releaseName:"astral-perturbation-4616")
  {
    id
    config
    urls
    {
      type
      url
    }

  }
}
```
By specifying a subfield of the `urls` type, the query executes successfully.

```
{
  "data": {
    "deployments": [
      {
        "id": "cjyem0p4m001a0b692dxk529v",
        "config": {
          "executor": "CeleryExecutor",
          "images": {
            "airflow": {
              "repository": "registry.demo.datarouter.ai/astral-perturbation-4616/airflow",
              "tag": "cli-5"
            }
          }
        },
        "urls": [
          {
            "type": "airflow",
            "url": "https://undefined-airflow.demo.datarouter.ai/"
          },
          {
            "type": "flower",
            "url": "https://undefined-flower.demo.datarouter.ai"
          }
        ]
      }
    ]
  }
}
```
**Note:** Custom types are often composed of other custom types.

## Adding System Admins
Mutations can be used to generate auth tokens, add system admins, and other things that `modify` the underlying database.

To add a system admin, the `id` of the user is needed. This can be obtained by an Admin with a `users` query.

```
query users {
  users(email:"pete@astronomer.io")
  {
    id    
  }
}
```
Grab the returned `id` and feed it into the next mutation.

Call `createSystemRoleBinding` with the proper inputs as shown.
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
