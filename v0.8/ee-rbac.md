---
title: "Assigning Access Roles"
description: "Using RBAC with Astronomer"
date: 2019-05-28T00:00:00.000Z
slug: "ee-rbac"
---

Astronomer v0.9.0 and beyond running supports role based access control (RBAC).

The Astronomer image comes bundled with an astronomer-security-manager package that connects permissions between
Houston (the Astronomer API) and Airflow's built in RBAC. Within a Workspace, you can now designate users a variety of permissions at the deployment-level.

## Overview

Astronomer supports three levels of Workspace roles: Admin, Editor, and Viewer.

To view roles within a Workspace, navigate to the `Users` tab.

![Users](https://assets2.astronomer.io/main/docs/astronomer-ui/users_permissions.png)

If you're a Workspace Admin, you can edit permissions by clicking into a user.

![Configure Access](https://assets2.astronomer.io/main/docs/astronomer-ui/configure_access.png)

## Astronomer Access

### Admin

Workspace Admins are the highest-tiered role. Admins can:

- Perform CRUD (create, read, update, delete) operations on the Workspace
- Perform CRUD operations on any deployment within that workspace
- Manage users and their permissions in a Workspace

### Editor

Behind admins, the Editor can:

- Perform CRUD operations on any deployment in the Workspace
- Perform CRUD operations on any service account in the Workspace

### Viewer

Viewers are limited to read-only mode. They can:

- Can view users in a Workspace
- Can view deployments in a Workspace

Viewers _cannot_ push code to a deployment.

**Note: By default, newly invited users are `Viewers` in a workspace.**

## Airflow Access

User roles apply to all Airflow deployments within a single Workspace.

### Admins

- Full access to the `Admin` panel in Airflow
- Full access to modify and interact with DAGs in the UI

### Editors

- Full access to modify and interact with DAGs in the UI
- Do *not* have access the `Admin` menu in Airflow, which includes:
    - Pools
    - Configuration
    - Users
    - Connections
    - Variables
    - XComs

![No Admin Tab](https://assets2.astronomer.io/main/docs/astronomer-ui/editor_view.png)

### Viewers

- Read-only access to the Airflow UI
- Cannot deploy to, modify, or delete anything within an Airflow deployment
- Any attempts to view logs, trigger DAGs, or anything else of the sort will result in a `403` and an `Access Denied` message.

![Access Denied](https://assets2.astronomer.io/main/docs/astronomer-ui/access_denied.png)

## Coming soon
We're rolling out Deployment level permissions to use in tandem with the Workspace level permissions!