---
title: "Managing Users on Astronomer Enterprise"
description: "Managing Users"
date: 2019-10-28T00:00:00.000Z
slug: "ee-managing-users"
---

# Adding Users to Astronomer

Once Astronomer Enterprise has been deployed, the first user to login is the System Admin by default. System Admins have access to the backend Grafana and Kibana dashboards and the platform-wide Admin view in our UI. 

Additional users can be added to Astronomer through email invites or by enabling public sign-ups. Users that try to access Astronomer without being invited while public sign-ups are disabled will be met with an error.

## Enabling Public Sign-Ups

Public sign-ups allow any user with access to the platform URL to create an account on the platform. Enabling this flag may be ideal in cases where SMTP credentials are tough to acquire, as disabling public sign-ups requires that a user accept an email invite.

Public sign-ups are a configuration available in Astronomer's Houston API and can be enabled in the `config.yaml` file of your Helm chart by including the below yaml snippet:

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

To push the new configuration, run a platform upgrade from the `helm.astronomer.io` repo:

```
$ helm ls
NAME                	REVISION	UPDATED                 	STATUS  	CHART                           	APP VERSION	NAMESPACE                                       
calico-crab         	4       	Fri Nov 22 09:36:51 2019	DEPLOYED	astronomer-platform-0.10.3-fix.1	0.10.3     	astro                    

$ helm upgrade calico-crab -f config.yaml . --namespace astro

```

## Platform Roles and Permissions 

A user on Astronomer Enterprise can be created by:

- Invitation to a Workspace via a Workspace Admin
- Invitation via a SystemAdmin
- Signing up via the Astronomer UI without an invitation (requires "Public Signups" be enabled)

Once a user exists on the platform, they can be invited to additional Workspaces and assigned a role within that particular Workspace, which applies to all Airflow Deployments within that Workspace. For a breakdown of Workspace Level Roles, refer to our [Role Based Access Control](https://www.astronomer.io/docs/rbac/) doc.

On Astronomer Enterprise, administrators of the platform can additionally customize the definitions of Workspace Level roles from the platform's config.yaml file. For guidelines, refer to our [Configuring Permissions](https://www.astronomer.io/docs/ee-configuring-permissions/) doc.

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
  users(email:"name@mycompany.com")
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
    userId: $id
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

