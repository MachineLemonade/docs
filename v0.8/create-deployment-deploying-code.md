---
title: "Deploying Your Code"
description: "Create your Airflow environment and push up your DAGs"
date: 2018-07-17T00:00:00.000Z
slug: "create-deployment-deploying-code"
---

## Creating a Deployment

The best place to create a deployment right now is directly from the UI.

From your workspace, click New Deployment and Configure your deployment accordingly!


Once that deployment is created, it should show up from your CLI as well (as long as you are pointing at the right workspace):

![Workspace Dashboard](https://s3.amazonaws.com/astronomer-cdn/website/img/guides/workspace_dashboard.png)


```
astro deployment list
 NAME           RELEASE NAME                 ASTRO      DEPLOYMENT ID                            
 demo_cluster     infrared-photon-7780     v0.7.5     c2436025-d501-4944-9c29-19ca61e7f359  
```

## Logging in and Deploying from the CLI

### Authentication

Before you can push your code up, you will need to authenticate.

If you are a Cloud customer:

```
astro auth login astronomer.cloud
```

If you are an Enterprise customer, your login command will be at the domain you chose to deploy on - e.g.

```
astro auth login airflow.MYCOMPANY.com
```

This will take you through our authentication flow:

```
 "Paolas-MBP-2:hello-astro paola$ astro auth login astronomer.cloud
 CLUSTER                             WORKSPACE                           
 astronomer.cloud                    4a6cb370-c361-440d-b02b-c90b07ef15f6

 Switched cluster
Username (leave blank for oAuth):
```

### Deployment

Once you've authenticated, make sure you are in the right workspace:

```
astro workspace switch
```

```
astro deployment list
 NAME           RELEASE NAME                 ASTRO      DEPLOYMENT ID                            
 BI Project     ultraviolet-isotope-9213     v0.7.5     c2436025-d501-4944-9c29-19ca61e7f359  
 ```

To deploy to an Airflow cluster, run:

```
astro airflow deploy
```

As you spin up additional deployments, they'll show up as options when you run `astro airflow deploy`

### What gets deployed?

Everything in your top level directory (and all children directory) that you ran `astro airflow init` in will get bundled into a Docker image and deployed out. We do **not** deploy any of the metadata associated with your the local airflow deployment - only the code.

For more information on what gets built into your image, jump over to the [CLI section](https://www.astronomer.io/docs/customizing-your-image/).


## Deployments, Workspaces, and Kubernetes Namespaces

### Kubernetes Namespaces

Airflow deployments live within their own Kubernetes [Namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) - each completely unaware of the rest. Each deployment is allocated separate resources, is configured in isolation, and maintains its own metadata. Whether it's ours on Astronomer Cloud or your own on Astronomer Enterprise, **the only thing deployments have in common is that they run on the same underlying Kubernetes cluster.**

### Organizing your Code

This is largely dependent on personal preference and your particular use case.

Generally, most use cases will call for a `production` and `dev` deployment, both of which exist within a single Workspace and therefore available to a set of users, each with varying permissions (as of Astronomer v0.9).

At a Workspace level, we recommend having 1 Astronomer Workspace per team of Airflow users. That way, anyone on each team has access to the same set of deployments under that Workspace (RBAC will soon allow you to adjust that access at a deployment level if you'd like). 

Across deployments, we'd generally recommend one repository/parent directory per project. That way, you leave the door open for CI/CD down the line if that's something you ever want to set up.

As for the code itself, we’ve seen effective organization where external code is partitioned by function and/or business case, so one directly for SQL, one for data processing tasks, one for data validation, etc.
