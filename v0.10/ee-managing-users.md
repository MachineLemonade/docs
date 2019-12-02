---
title: "Managing Users on Astronomer Enterprise"
description: "Managing Users"
date: 2019-10-28T00:00:00.000Z
slug: "ee-managing-users"
---

# Adding Users to Astronomer
Once Astronomer Enterprise has been deployed, the first user to login is the `system admin`. System admins have access to the backend Grafana and Kibana views, as well as the Admin panel. 

Additional users can be added to Astronomer through email invites or by enabling public sign ups. Users that try to access Astronomer without being invited while public sign-ups is disabled with get a 500 error.

## Enabling Public Sign Ups
Public signups allow any user with access to the URL that Astronomer is hosted at to create a workspace and access the platform. This may be ideal to enable in cases where SMTP credentials are tough to acquire or initially onboarding users within an org.

Public sign-ups are a Houston (Astronomer's API) configuration and can be enabled in the `config.yaml` file by adding:

```
astronomer:
  houston:
    config:
      publicSignups: true
      emailConfirmation: false
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

Once is invited or signs up, they can be added to additional workspaces with different permissions. The [Role Based Access Control](https://www.astronomer.io/docs/rbac/) breaks down the different roles available.

[Customizations to each role](https://www.astronomer.io/docs/ee-configuring-permissions/) can also be made on from the config.yaml file.

## Adding System Admins
System admins can be added by directly issuing an API call to Houston. Systems admins can [directly query houston from the GraphQL playground](https://www.astronomer.io/docs/houston-api/)

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
Users can verify they are system admins by navigating to `grafana.BASEDOMAIN` or `kibana.BASEDOMAIN` - non admin users will be redirected to the `app.BASEDOMAIN` page, whereas admins will have access to these dashboards.

Note that other system admins can add additional system admins.

