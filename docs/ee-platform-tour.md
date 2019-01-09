---
title: "Platform Tour"
description: "Walking through the Astronomer Platform."
date: 2018-10-12T00:00:00.000Z
slug: "ee-platform-tour"
menu: ["Enterprise Edition"]
position: [3]
---

Now that you've deployed your first DAG, let's walk through each aspect of the Astronomer Platform:

## Orbiter UI

Orbiter, or the `app.BASEDOMAIN` page is the first view you'll see when you log into Astronomer. This will be the default view you will use to manage your workspaces, deployments, and users. You're also able to configure and scale each of your Airflow deployments from here. (Soon, you'll be able to see logs and metrics in this view!)

If you are setting up Astronomer for your org, check out our guide on managing workspaces and deployments.


### Houston API

Under the hood, our [houston-api](https://github.com/astronomer/houston-api) is the brain of our platform.

If you navigate to `houston.BASEDOMAIN/playground` you'll be able to interact with the platform through GraphQL queries. You can find some examples in our [houston-api section](https://www.astronomer.io/docs/houston-api/) section.


![Deployment Page](https://assets2.astronomer.io/guides/docs/ee/houston_example.png)

### Grafana Dashboards

Astronomer Enterprise provides single pane dashboards that let you see how each piece of the Airflow stack is performing, along with a few "summary views."

You can check out the queries used for each dashboard here, as well as get more information in the

Note that these views are only available to admins and the first person to authenticate to your cluster will be the system admin.


![Deployment Page](https://assets2.astronomer.io/guides/docs/ee/airflow_deployment_overview.png)
