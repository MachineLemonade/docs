---
title: "Enterprise Quickstart"
description: "Quickstart with Astronomer Enterprise"
date: 2018-07-17T00:00:00.000Z
slug: "ee-getting-started"
---


# Getting Started with Astronomer Enterprise:

_If your org just started running Astronomer Enterprise, this is the doc you will want to start with._

<iframe width="560" height="315" src="https://www.youtube.com/embed/02au2O3vDTk" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


### 1. Start with Astronomer Cloud

At its core, Astronomer Cloud is a large-scale deployment of Astronomer Enterprise that is fully managed by our team. Cloud provides parallel Airflow functionality to Enterprise with just a few differences.

Astronomer Cloud:

- Runs in Astronomer's VPC and uses the public internet, whereas Astronomer Enterprise will run in *your* environment according to your own security settings
- Is billed by usage, whereas Enterprise is billed through an annual license
- Does not give users access to the back-end Prometheus/Grafana/Kibana monitoring stack

To get a sense of the Astronomer user experience, try out Cloud by [starting a 14-Day Trial](https://www.astronomer.io/trial/).

### 2. Install Astronomer Enterprise

If you are in charge of setting up Astronomer for your org, head over to our [Enterprise Edition](https://www.astronomer.io/docs/ee-overview/) section for get Astronomer running on your Kubernetes Cluster!


### 3. Install the CLI

Run:

```
curl -sSL https://install.astronomer.io | sudo bash

```

**Note:** The `curl` command will work for Unix (Linux+Mac) based systems. If you want to run on Windows 10, you'll need to run through [this guide](https://www.astronomer.io/docs/cli-installation-windows-10/?_ga=2.105008643.146962510.1554994254-1828434170.1536931577) on getting Docker for WSL working.


Let's make sure you have Astro CLI installed on your machine, and that you have a project to work from.

```bash
astro
```

If you're set up properly, you should see the following:

```
astro is a command line interface for working with the Astronomer Platform.

Usage:
  astro [command]

Available Commands:
  airflow     Manage airflow projects and deployments
  auth        Mangage astronomer identity
  cluster     Manage Astronomer EE clusters
  config      Manage astro project configurations
  deployment  Manage airflow deployments
  help        Help about any command
  upgrade     Check for newer version of Astronomer CLI
  user        Manage astronomer user
  version     Astronomer CLI version
  workspace   Manage Astronomer workspaces

Flags:
  -h, --help   help for astro
```

### Create a project

Your first step is to create a project to work from that lives in a folder on your local machine. The command you'll need is listed below, with an example `hello-astro` project.

 ```
mkdir hello-astro && cd hello-astro
astro dev init
 ```

### 3. Find your basedomain and login

Since Astronomer is running entirely on your infrastructure, it will be located at a subdomain specific to your organization. Most of our customers will deploy something to `airflow.COMPANY.com`, but ask your Kubernetes person or ping us on Slack to find out for sure. Head to `app.BASEDOMAIN` to login - you'll see something like this:

![Account Dashboard](https://s3.amazonaws.com/astronomer-cdn/website/img/guides/account_dashboard.png)


### 4. Authenticate from the CLI

You can authenticate with

`astro auth login BASEDOMAIN`

and run through the authentication flow that was set up (most likely be the OAuth flow). You'll be prompted for the workspace that you want to log into - as you are added to more workspaces, there will be more values on this prompt.

### 5. Start Airflow locally

Now if you run `astro dev start` from that directory, you'll see an image built and running on `localhost:8080/admin`.You can write dags in the `dags` directory and plugins in the `plugins` directory and these changes will be picked up automatically. For additional configurations, check out our CLI doc on [customizing your image](https://www.astronomer.io/docs/customizing-your-image/).


### 6. Spin up an environment and deploy your code

If you are the first user of Astronomer within your org, you will need to create a Deployment in your workspace.

Check out our doc on the [Astromomer UI](https://www.astronomer.io/docs/astronomer-ui/) and [Creating Deployments](https://www.astronomer.io/docs/create-deployment-deploying-code/) for a complete walkthrough.


### 7. **Optional** Admin tools

If you are the first person to log onto Astronomer in your org, you will have access to the admin Grafana and Kibana Dashboards. Head to `kibana.BASEDOMAIN` and `grafana.BASEDOMAIN` for single pane views of all the metrics and logs going through your platform.
