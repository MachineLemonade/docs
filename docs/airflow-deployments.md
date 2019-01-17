---
title: "Airflow Deployments"
date: 2018-10-12T00:00:00.000Z
slug: "airflow-deployments"
menu: ["root"]
position: [5]
---

If you're just getting started on Astronomer, you'll want to have a solid grasp on common terminology specific to both Apache Airflow and our platform. In this guide, you'll find some general definitions to start followed by a more in-depth breakdown.

## Basic Definitions

**Astronomer Workspace** = A personal or shared space on Astronomer’s platform that is home to a collection of Airflow deployments. User access to deployments is managed at the workspace level on Astronomer.

**Airflow Deployment** = A single instance of Apache Airflow made up of a scheduler, a webserver, and one or more workers. A deployment has the capacity to host a collection of DAGs, and sits on top of a corresponding Kubernetes cluster.

## Workspace Layer

### Overview 
A `Workspace` is an Astronomer-specific term. You can think of your workspaces the same way you'd think of teams - they're just collections of Airflow deployments that specific user groups have access to. When you create an account on Astronomer, a default personal workspace is automatically created. Airflow deployments are hierarchically lower - from a workspace, you can create one or more Airflow deployments, and grant or restrict user access to those deployments accordingly.

### Deployments and Workspaces

If you were a solo agent, you could have multiple Airflow deployments within that single workspace and have no need for additional workspaces. Teams, however, often share one or more workspaces labeled as such, and have multiple Airflow deployments from there. To invite a team member,they first have to create their own account [here](https://app.astronomer.cloud/signup) before they can be invited to an additional or shared workspace.

Deployments cannot be used or shared accross workspaces. While you’re free to push local DAGs and code anywhere you wish at any time, there is currently no way to move an existing Airflow instance from one workspace to another once deployed.

## Deployment Layer

### Overview

In the context of Astronomer, the term `Airflow Deployment` is used to describe an instance of Airflow that you've spun up either via our [app UI](https://astronomer.io/docs/overview) or [CLI](https://astronomer.io/docs/cli-getting-started) as part of a workspace. Under the hood, each deployment gets its own Kubernetes namespace and has a set isolated resources reserved for itself.

For Cloud customers, that cluster is hosted on Astronomer. For Enterprise customers, that cluster is hosted on your own Kubernetes.

### Deployment Resources

With [Astronomer v0.7](https://www.astronomer.io/blog/astronomer-v0-7-0-release-notes/), you're now able to adjust the resources given to your Airflow deployment directly from our app's UI. This functionality allows you to choose executor (local or celery) and easily provision additional resources as you scale up.

Resources aside, you won’t technically see any limitations or maximums on your deployment. Airflow is designed to run as much as resources to that environment permit.


