---
title: "Assigning Access Roles"
description: "Using RBAC with Astronomer"
date: 2018-10-12T00:00:00.000Z
slug: "ee-rbac"
---

Astronomer 0.9.0 (running Airflow 1.10.3 or later) and beyond supports role based access control (RBAC).
The Astronomer image comes bundled with an astronomer-security-manager package that connects permission between
Houston (the Astronomer API) and Airflow's built in RBAC.

## Roles

 Roles can be viewed and edited from the `Users` tab in a Workspace.
![Users](https://assets2.astronomer.io/main/docs/astronomer-ui/users_permissions.png)

Astronomer supports 3 levels of workspace roles; Admin, Editor, and Viewer:

![Configure Access](https://assets2.astronomer.io/main/docs/astronomer-ui/configure_access.png)


### Admin
Workspace admins are the highest role and have the ability to:

- Perform CRUD (create, read, update, delete) operations on the Workspace
- Perform CRUD operations on any deployment in the workspace
- Manage users and their permissions in a Workspace.

### Editor
Behind admin, the editor role will let you:

- Perform CRUD operations on any deployment in the workspace
- Perform CRUD operations on any service account in the workspace

### Viewer
Finally, viewers are able to:

- View users in a workspace
- View deployments in a workspace

**Note: By default, newly invited users are `Viewers` in a workspace.**

Only Admins and Editors can push code to a deployment - Viewers are in read only mode.

## Using Airflow
Workspace roles filter down into each Airflow deployment in a Workspace.

Admins have full access to the `Admin` panel in Airflow, as well as permissions to interact with any of the DAGs in the UI.

Similarly, `Editors` will be able to interact with DAGs in the Airflow UI. However, `Editors` will **not** have access to the `Admin` tab in Airflow:

![No Admin Tab](https://assets2.astronomer.io/main/docs/astronomer-ui/editor_view.png)


Viewers will not be able to change anything in an Airflow deployment - any attempts to view logs, trigger DAGs, or anything else of the sort will result in a `403` and an `Access Denied` message.

![Access Denied](https://assets2.astronomer.io/main/docs/astronomer-ui/access_denied.png)

## Coming soon
We're rolling out Deployment level permissions to use in tandem with the Workspace level permissions!
