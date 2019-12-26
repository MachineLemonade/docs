---
title: "Managing Users on Astronomer Enterprise"
description: "Managing Users"
date: 2019-10-28T00:00:00.000Z
slug: "ee-managing-users"
---

## Overview

### Adding Users to Astronomer

When Astronomer Enterprise is first deployed, the first user to login is a "System Admin" by default. From there, a user on Astronomer Enterprise can be created by:

- Invitation to a Workspace by a Workspace Admin
- Invitation to Astronomer by a System Admin
- Signing up via the Astronomer UI without an invitation (requires "Public Signups")

On Astronomer, administrators have the option to either open the platform to public signups or limit signups to users invited by others via email.

Once a user exists on the platform, administrators can leverage Astronomer's Role Based Acess Control (RBAC) to manage users.

### Role-Based Access Control

On Astronomer, users can be assigned 2 levels of roles:

1. Workspace Role (Viewer, Editor, Admin)
2. System Role (System Admin)

Workspace roles apply to all Airflow Deployments within a single Workspace, whereas System Roles apply to *all* Workspaces across a single cluster.

For a detailed breakdown of the 3 Workspace Level Roles on Astronomer (Viewer, Editor and Admin), refer to our [Role Based Access Control](https://www.astronomer.io/docs/rbac/) doc.

For more information on Public Signups, role customization and assigning users System Admin permissions, read below.

## Public Signups

As noted above, Public Signups allow any user with access to the platform URL (the Astronomer UI) to create an account. If Public Signups are *disabled*, users that try to access Astronomer without an invitation from another user will be met with an error.

In cases where SMTP credentials are difficult to acquire, enabling this flag might facilitate initial setup, as disabling public signups requires that a user accept an email invitation.

### Enabling Public Signups

Public Signups are a configuration available in Astronomer's Houston API and can be enabled in the `config.yaml` file of your Helm chart.

#### Modify your config.yaml

To *enable* Public Signups, add the following yaml snippet to your `config.yaml` file:

```
astronomer:
  houston:
    config:
      publicSignups: true
      emailConfirmation: false # If you wish to also disable other SMTP-dependent features
```

An example `config.yaml` would look like:

```
global:
  baseDomain: mybasedomain
  tlsSecret: astronomer-tls
nginx:
  loadBalancerIP: 0.0.0.0
  preserveSourceIP: true

astronomer:
  houston:
    config:
      publicSignups: true
      emailConfirmation: false

```

#### Run a Platform Upgrade

To push the new configuration, run a platform upgrade from the `helm.astronomer.io` repo:

```
$ helm ls
NAME                	REVISION	UPDATED                 	STATUS  	CHART                           	APP VERSION	NAMESPACE                                       
calico-crab         	4       	Fri Nov 22 09:36:51 2019	DEPLOYED	astronomer-platform-0.10.3-fix.1	0.10.3     	astro                    

$ helm upgrade calico-crab -f config.yaml . --namespace astro

```

## Workspace Role Customization 

On Astronomer Enterprise, platform administrators can customize the definitions of Workspace Level roles from the same `config.yaml` file.

For guidelines, refer to our [Configuring Permissions](https://www.astronomer.io/docs/ee-configuring-permissions/) doc.

## System Admin Configuration

### Overview

The System Admin role on Astronomer Enterprise brings a range of cluster-wide permissions that supercedes Workspace-level access and allows a user to monitor and take action across Workspaces, Deployments and Users within a single cluster.

On Astronomer, System Admins can:

- List and search *all* users
- List and search *all* deployments
- Access the Airflow UI for *all* deployments
- Delete a user
- Delete an Airflow Deployment
- Access Grafana and Kibana for cluster-level monitoring
- Add other System Admins

By default, the first user to log into an Astronomer Enterprise installation is granted the System Admin permission set.

Read below for guidelines on assigning additional users the System Admin role.

### Adding a System Admin

System Admins can be added to Astronomer Enterprise by issuing an API call to Houston via the [GraphQL playground](https://www.astronomer.io/docs/houston-api/).

Keep in mind that:
- Only existing System Admins can grant the SysAdmin role to another user
- The user must have a verified email address and already exist in the system

#### Query for a User's `uuid`

The API call to add a System Admin on Astronomer requires the `uuid` of the user in question.

To pull the user's `uuid`, run the following query with their email address as the input:

```
query GetUser {
  users(email:"<name@mycompany.com>")
  {
    uuid
    roleBindings {role}   
  }
}
```

In the output, you should see:

- The user's `uuid`
- A list of existing roles across the cluster (e.g. Workspace Admin)

> **Note:** You'll have to authenticate to the Houston API to be able to run the query above. For guidelines, refer to our [Houston API doc](https://www.astronomer.io/docs/houston-api/).

#### Call the `createSystemRoleBinding` Mutation

Below the query above, call `createSystemRoleBinding` with the `uuid` you pulled above.

The mutation should look like:

```
mutation AddAdmin {
  createSystemRoleBinding(
    userId: "<uuid>"
    role: SYSTEM_ADMIN
  ) {
    id
  }
}
```

#### Verify SysAdmin Access

To verify a user was successfully granted the SysAdmin role, ensure they can do the following:

- Navigate to `grafana.BASEDOMAIN`
- Navigate to `kibana.BASEDOMAIN`
- Access the "Admin Settings" tab from the top right menu of the Astronomer UI