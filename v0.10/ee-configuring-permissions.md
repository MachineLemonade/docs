---
title: "Configuring Permissions"
description: "Applying custom permission mappings to roles in Astronomer Enterprise."
date: 2019-11-16T00:00:00.000Z
slug: "ee-configuring-permissions"
---

The Astronomer platform ships with a collection of roles that can be applied to each user. Each role is given a list of permissions that apply to certain GraphQL mutations, allowing each user to perform certain actions and blocking them from performing others. In this doc, we'll cover what each permission allows a user to do, what permissions are applied to each role by default, and how to change those permissions via Helm so that you can fully customize roles in your Astronomer Enterprise installation.


## Permissions Reference

Permissions are defined as `scope.entity.action`, where the `scope` is the layer of our application to which the permission applies, the `entity` is the object being operated on, and the `action` is the verb describing what is being done to the `entity`. To view all available platform permissions, view our [default Houston API configuration](https://github.com/astronomer/houston-api/blob/master/config/default.yaml#L200). Each permission is applied to the role under which it's listed and permissions from lower-level roles cascade up to higher-level roles. For example, a `SYSTEM_ADMIN` can do the things listed under its role _and_ all things listed under the `SYSTEM_EDITOR` and `SYSTEM_VIEWER` roles.

## Roles and Permissions

Roles can be bound to individual users via the Houston API or UI. For a reference on how to change a user's role via the GraphQL playground, see our [Houston API doc](https://astronomer.io/docs/houston-api).

Because our roles are constantly being expanded as we add more features to the platform, we will refrain from covering which permissions apply to which roles in this doc. Rather, you can [view our API configuration directly](https://github.com/astronomer/houston-api/blob/master/config/default.yaml#L200)or the latest on these roles and how they relate to our application permissions.

## Customizing Permissions

Because our API configuration is completely customizable for Enterprise installs, you can control which permissions are applied to each role within your custom implementation of Astronomer. To do that, follow the steps below:

1.  Examine our default roles and permissions and identify which ones you would like to change. This will involved either removing specific permissions that exist on roles or adding them to roles where they do not exist.

2. Apply those configuration updates via the following changes to your `values.yaml` Helm file:

```yaml
astronomer:
  houston:
    config:
      roles:
        DEPLOYMENT_EDITOR: # Note that you can apply these changes to any role
          permissions:
            deployment.images.push: false # Note that any permissions can be added or removed from this role via this syntax
```


             