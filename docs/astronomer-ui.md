---
title: "The Astronomer UI"
description: "A walkthrough of the Astronomer App"
date: 2018-10-12T00:00:00.000Z
slug: "astronomer-ui"
---

We've designed the Astronomer UI as a place for you to easily and effectively manage users, deployments and resources.

If you're just getting started on Astronomer, you'll want to have a solid grasp of how to navigate [the Astronomer app](https://app.astronomer.cloud/deployments) and best leverage it for your use of Airflow.

In this guide, you'll find some general definitions of Astronomer-specific terminology as well as a walkthrough of each layer of our platform's UI.

# Overview

## Basic Definitions

If you have an account on Astronomer, you'll need to be familiar with two basic terms:

**Astronomer Workspace** = A personal or shared space on Astronomer’s platform that is home to a collection of Airflow deployments. User access to deployments is managed at the workspace level on Astronomer.

**Airflow Deployment** = A single instance of [Apache Airflow](https://airflow.apache.org/) made up of a scheduler, a webserver, and one or more workers. A deployment has the capacity to host a collection of DAGs, and sits on top of a corresponding Kubernetes cluster.

## Workspace Layer

### Overview
A `Workspace` is an Astronomer-specific term. You can think of your workspaces the same way you'd think of teams - they're just collections of Airflow deployments that specific user groups have access to. When you create an account on Astronomer, a default personal workspace is automatically created. Airflow deployments are hierarchically lower - from a workspace, you can create one or more Airflow deployments, and grant or restrict user access to those deployments accordingly.

### Deployments and Workspaces

If you were a solo agent, you could have multiple Airflow deployments within that single workspace and have no need for additional workspaces. Teams, however, often share one or more workspaces labeled as such, and have multiple Airflow deployments from there.

Deployments cannot be used or shared accross workspaces. While you’re free to push local DAGs and code anywhere you wish at any time, there is currently no way to move an existing Airflow instance from one workspace to another once deployed.

## Deployment Layer

### Overview

In the context of Astronomer, the term `Airflow Deployment` is used to describe an instance of Airflow that you've spun up either via our [app UI](https://astronomer.io/docs/overview) or [CLI](https://astronomer.io/docs/cli-getting-started) as part of a workspace. Under the hood, each deployment gets its own Kubernetes namespace and has a set isolated resources reserved for itself.

For Cloud customers, that cluster is hosted on Astronomer. For Enterprise customers, that cluster is hosted on your own Kubernetes.

### Deployment Resources

With [Astronomer v0.7](https://www.astronomer.io/blog/astronomer-v0-7-0-release/), you're now able to adjust the resources given to your Airflow deployment directly from our app's UI. This functionality allows you to choose executor (local or celery) and easily provision additional resources as you scale up.

Resources aside, you won’t technically see any limitations or maximums on your deployment. Airflow is designed to run as much as resources to that environment permit.

# The Astronomer UI

To help achieve Astronomer's goal of improving Airflow's usability, we have built a custom UI that makes user access and deployment management dead simple. In this guide, we'll walk through the specific components of the Astronomer UI and discuss the design principles that led to their creation.

## Getting Started

### Account Dashboard

New to Astronomer? Check out [this guide](https://www.astronomer.io/docs/getting-started/) first to get started.

Once logged in, you'll land on a dashboard that gives you an overview of your Workspaces. We'll call this the `Account Dashboard`:

![Account Dashboard](https://s3.amazonaws.com/astronomer-cdn/website/img/guides/account_dashboard.png)

From this dashboard, you can:

1. Spin up new Workspaces
2. View the workspaces you currently have access to
3. Adjust your account name under the `Personal Settings` tab

### Workspace Dashboard

Once you click into a workspace, you'll land on another dashboard that we'll call the `Workspace Dashboard`:

![Workspace Dashboard](https://s3.amazonaws.com/astronomer-cdn/website/img/guides/workspace_dashboard.png)

Here, you have a high-level overview of all of the active Airflow deployments you have running in that given workspace. In this case, we only have one cluster spun up.

From this screen, you can:

1. Create new Airflow deployments
2. Manage user access to the workspace
3. Generate tokens for CI/CD systems via service accounts.

**Note:** Since all of our app activity is routed through a GraphQL API, you're free to create deployments, switch workspaces, and add users via our [CLI](https://www.astronomer.io/docs/cli-getting-started/) if you prefer staying in your terminal.

### User Management

If you navigate over to the `Users` tab of your Workspace Dashboard, you'll be able to see who has access to the Workspace. If you'd like to share access to other members of your organization, invite them to a workspace you're a part of. Once members, they'll have access to all Airflow deployments under that workspace (deployment-level permissions coming soon).

**Note:** If you'd like to invite a user to your workspace, they must first [create an account on Astronomer](https://app.astronomer.cloud/signup).

![Users](https://s3.amazonaws.com/astronomer-cdn/website/img/guides/user_dashboard.png)

## Deployments

From the Workspace dashboard, navigate back to the `Deployments` tab.

If you click into one of your Airflow deployments, you'll land on a page that looks like this:

![Deployments](https://s3.amazonaws.com/astronomer-cdn/website/img/guides/deployment_dashboard.png)

From here, you'll be able to access:

1. Airflow UI (DAG Dashboard)
2. Flower dashboard

For a breakdown the Airflow UI itself, check out [this guide](https://www.astronomer.io/guides/airflow-ui/).

### Deployment Configuration

If you jump into the `Configure` tab on the deployment overview page, you'll be able to:

1. Change the name + description of your deployment
2. See what version of Airflow + Astronomer your deployment is running
3. Insert environment variables (*new*)
4. Deprovision your deployment

This tab also allows you to adjust your resource components - empowering you to freely scale your deployment up or down as you wish. To this end, you can:

1. Choose your executor (local or celery)
2. Adjust worker count
3. Add extra capacity to your cluster
4. Adjust worker termination grace period

By default, workers on your Astronomer deployment will run with 3.75GB, 1 CPU.

Wondering what resources you need to start? It's hard to say, but we're happy to chat through your use case. Reach out to support@astronomer.io to set something up with us.
