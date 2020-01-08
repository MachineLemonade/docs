---
title: "Configuring Permissions"
description: "Applying custom permission mappings to roles in Astronomer Enterprise."
date: 2019-11-16T00:00:00.000Z
slug: "ee-configuring-permissions"
---

The Astronomer platform ships with a collection of roles that can be applied to each user. Each role is given a list of permissions that allow access to certain GraphQL mutations, allowing each user to perform certain actions and blocking them from performing others. In this doc, we'll go over how to find those permissions, what permissions are applied to each role by default, and how to change those permissions via Helm so that you can fully customize user access in your Astronomer Enterprise installation.


## Permissions Reference

Permissions are defined in our default Helm charts as `scope.entity.action`, where the `scope` is the layer of our application to which the permission applies, the `entity` is the object being operated on, and the `action` is the verb describing the operation being performed on the `entity`. To view all available platform permissions, view our [default Houston API configuration](https://github.com/astronomer/houston-api/blob/master/config/default.yaml#L200). Each permission is applied to the role under which it is listed and permissions from lower-level roles cascade up to higher-level roles. For example, a `SYSTEM_ADMIN` can do the things listed under its role _and_ all things listed under the `SYSTEM_EDITOR` and `SYSTEM_VIEWER` roles because of the [cascade applied in the permission list](https://github.com/astronomer/houston-api/blob/v0.10.3/config/default.yaml#L229).

## Roles and Permissions

Roles can be bound to individual users via the Houston API or Orbit UI.

Because our roles are constantly being expanded upon as we add more features to the platform, we will refrain from covering which permissions apply to which roles in this doc. Rather, you can check out our [User Roles and Permissions doc](https://www.astronomer.io/docs/rbac/) for a high-level overview on the capabilities allowed for each role. If you'd like a deeper dive, you can [view our API configuration directly](https://github.com/astronomer/houston-api/blob/v0.10.3/config/default.yaml#L200)or the latest on these roles and how they map to our individual permissions.

> **Note:** In the current state of our platform, all `DEPLOYMENT` roles are synthetically mapped to `WORKSPACE` roles, meaning a `WORKSPACE_EDITOR` can *also* do what a `DEPLOYMENT_EDITOR` can. This is to set the stage for deployment-level permissions, which we will expose via our API and UI in an upcoming platform release.

## Customizing Permissions

Because our API configuration is completely customizable for Enterprise installs, you can control which permissions are applied to each role within your implementation of Astronomer. This can be accomplished via the following steps:

**1. Identify Default Roles**  

Examine our [default roles and permissions](https://github.com/astronomer/houston-api/blob/v0.10.3/config/default.yaml#L200) and identify which ones you would like to change. This will involved either removing specific permissions that exist on roles or adding them to roles where they do not exist.

**2. Apply Changes via Helm** 

Apply those configuration updates via the following changes to your `config.yaml` Helm file. Note that you can apply this concept to any role/permission, but for the purposes of this doc we'll use `DEPLOYMENT_EDITOR` and `deployment.images.push` as an example. In this case, the user is disallowing `DEPLOYMENT_EDITORS` (and therefore `WORKSPACE_EDITORS`) from deploying code directly to an Airflow instance. This might be done to enforce CI/CD over direct deploys from our CLI for all editors. Note that in v0.10.x of the platform, users will need to copy and paste the entire role block into their `config.yaml`, but we have a more [elegant way](https://github.com/astronomer/houston-api/pull/170#issuecomment-554463343) of tweaking these permissions that will be introduced in v0.11 of the platform.

It's not easy to see given that before our new feature is introduced we need to copy all roles into `config.yaml` for changes to propagate, but, in the snippet below, [we've removed the `deployment.images.push` permission from the `DEPLOYMENT_EDITOR` role](https://github.com/astronomer/houston-api/blob/v0.10.3/config/default.yaml#L302).

```yaml
astronomer:
  houston:
    config:
      roles:
        #
        # System
        #
        - id: SYSTEM_ADMIN
          name: System Admin
          permissions:
            - system.deployments.get
            - system.deployments.update
            - system.deployments.delete
            - system.deployments.logs
            - system.deployments.metrics
            - system.iam.update
            - system.invite.get
            - system.monitoring.get
            - system.serviceAccounts.get
            - system.serviceAccounts.create
            - system.serviceAccounts.update
            - system.serviceAccounts.delete
            - system.users.get
            - system.user.invite
            - system.user.delete
            - system.user.verifyEmail
            - system.workspace.addCustomerId
            - system.workspace.suspend
            - system.workspace.extendTrial
            - system.airflow.admin

        - id: SYSTEM_EDITOR
          name: System Editor
          permissions:
            - system.iam.update
            - system.monitoring.get
            - system.serviceAccounts.get
            - system.serviceAccounts.update
            - system.airflow.user

        - id: SYSTEM_VIEWER
          name: System Viewer
          permissions:
            - system.monitoring.get
            - system.serviceAccounts.get
            - system.airflow.get

        #
        # Workspace
        #
        - id: WORKSPACE_ADMIN
          name: Workspace Admin
          permissions:
            - workspace.billing.update
            - workspace.config.update
            - workspace.config.delete
            - workspace.deployments.get
            - workspace.deployments.create
            - workspace.iam.update
            - workspace.invites.get
            - workspace.serviceAccounts.get
            - workspace.serviceAccounts.create
            - workspace.serviceAccounts.update
            - workspace.serviceAccounts.delete
            - workspace.users.get

        - id: WORKSPACE_EDITOR
          name: Workspace Editor
          permissions:
            - workspace.config.update
            - workspace.invites.get
            - workspace.deployments.get
            - workspace.deployments.create
            - workspace.serviceAccounts.get
            - workspace.serviceAccounts.create
            - workspace.serviceAccounts.update
            - workspace.serviceAccounts.delete
            - workspace.users.get

        - id: WORKSPACE_VIEWER
          name: Workspace Viewer
          permissions:
            - workspace.deployments.get
            - workspace.invites.get
            - workspace.serviceAccounts.get
            - workspace.users.get

        #
        # Deployment
        #
        - id: DEPLOYMENT_ADMIN
          name: Deployment Admin
          permissions:
            - deployment.airflow.user
            - deployment.airflow.get
            - deployment.config.get
            - deployment.config.update
            - deployment.config.delete
            - deployment.images.push
            - deployment.airflow.admin
            - deployment.logs.get
            - deployment.metrics.get
            - deployment.serviceAccounts.get
            - deployment.serviceAccounts.create
            - deployment.serviceAccounts.update
            - deployment.serviceAccounts.delete

        - id: DEPLOYMENT_EDITOR
          name: Deployment Editor
          permissions:
            - deployment.airflow.user
            - deployment.airflow.get
            - deployment.config.get
            - deployment.config.update
            - deployment.logs.get
            - deployment.metrics.get
            - deployment.serviceAccounts.get
            - deployment.serviceAccounts.create
            - deployment.serviceAccounts.update
            - deployment.serviceAccounts.delete

        - id: DEPLOYMENT_VIEWER
          name: Deployment Viewer
          permissions:
            - deployment.airflow.get
            - deployment.config.get
            - deployment.logs.get
            - deployment.metrics.get
            - deployment.serviceAccounts.get


```


**3. Upgrade the Cluster**

Once you have your `config.yaml` updated, you can propigate these changes to your cluster by running the following command:

```bash
helm upgrade <platform-name> -f config.yaml . --namespace <namespace>
```

             