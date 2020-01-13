---
title: "Managing Users on Astronomer Enterprise"
description: "Managing Users"
date: 2019-10-28T00:00:00.000Z
slug: "ee-managing-users"
---

## Overview

In addition to the [Role-Based Access Control (RBAC) functionality](https://www.astronomer.io/docs/rbac/) core to our platform, Astronomer Enterprise allows teams to customize *how* they want users to create accounts on Astronomer and what they're able to do on the platform - both on Astronomer and Airflow.

Read below for a high-level overview of user management and guidelines around public sign-ups, role customization and adding System Admins.

### Adding Users to Astronomer

When Astronomer Enterprise is first deployed, the first user to log in is granted "System Admin" permissions by default. From there, a user is created on Astronomer Enterprise by:

- Invitation to a Workspace by a Workspace Admin
- Invitation to Astronomer by a System Admin
- Signing up via the Astronomer UI without an invitation (requires "Public Sign-Ups")

On Astronomer, administrators have the option to either open the platform to public sign-ups or limit sign-ups to users invited by others.

### Managing Users

Once on the platform, administrators can customize permissions across teams. On Astronomer, users can be assigned roles at 2 levels:

1. Workspace Level (Viewer, Editor, Admin)
2. System Level (System Admin)

Workspace roles apply to all Airflow Deployments within a single Workspace, whereas System Roles apply to *all* Workspaces across a single cluster. For a detailed breakdown of the 3 Workspace Level Roles on Astronomer (Viewer, Editor and Admin), refer to our [Role Based Access Control](https://www.astronomer.io/docs/rbac/) doc.

## Public Sign-Ups

As noted above, public sign-ups allow any user with access to the platform URL (the Astronomer UI) to create an account. If Public sign-ups are *disabled*, users that try to access Astronomer without an invitation from another user will be met with an error.

In cases where SMTP credentials are difficult to acquire, enabling this flag might facilitate initial setup, as disabling public sign-ups requires that a user accept an email invitation.

### Enabling Public Sign-Ups

Public Sign-Ups are a configuration available in Astronomer's Houston API and can be enabled in the `config.yaml` file of your Helm chart.

#### Modify your Configuration

To *enable* Public Sign-Ups, add the following yaml snippet to your `config.yaml` file:

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

## System Admins

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

#### Query for a User's ID

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

#### Run the Mutation

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


## System View-Only Users

By default, all users on Astronomer have the ability to create new workspaces. Since users are assigned the `WORKSPACE_ADMIN` role by default when they create a workspace, that user will then be able to spin up new Airflow deployments within that workspace.

Some teams might want to limit a user's access so that they do not have the ability to do this so that they reserve access to creating workspaces to a specific sub-group of users. This can be accomplished by leveraging our platform's `USER` role. 

Our platform ships with a `USER` role that is synthetically bound to all users. By default, this [role includes the `system.workspace.create` permission](https://github.com/astronomer/houston-api/blob/master/config/default.yaml#L324), which allows all users to create new workspaces on the platform. In order to change this and make it so that all users _are not_ able to create workspaces, you can remove that permission from the role and add it onto a separate role of your choice- this will likely be the `SYSTEM_ADMIN` role if you would prefer that admins manage how resources are provisioned across the cluster.

To configure and apply this change, follow the steps in our [Configuring Permissions](https://www.astronomer.io/docs/ee-configuring-permissions/) doc.

## Customizing Roles and Permissions 

On Astronomer Enterprise, platform administrators can customize the definitions of Workspace Level roles from the same `config.yaml` file.

For guidelines, refer to our [Configuring Permissions](https://www.astronomer.io/docs/ee-configuring-permissions/) doc.