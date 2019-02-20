---
title: "Getting Started"
description: "How to get up and running with Astronomer"
date: 2018-10-12T00:00:00.000Z
slug: "getting-started"
---

Welcome to Astronomer.

We're here to kick off your trial on Astronomer by walking you through a sample DAG deployment. Whether you're exploring our [Enterprise](https://astronomer.io/enterprise) or [Cloud](https://astronomer.io/cloud) offering, it's a great way to get to know our platform.

## Start with the CLI

### Install

Let's begin by downloading our open-source CLI so you can start developing locally.

Be sure that you have [Docker](https://www.docker.com/) and [Go](https://golang.org/) installed on your machine, then open your terminal and run

```
 curl -sSL https://install.astronomer.io | sudo bash
 ```

If you run into issues, check out our [CLI Install guide](https://www.astronomer.io/docs/cli-installation/).

### Initialize your Airflow Project

Create a new project directory somewhere on your computer where we'll store all of the files necessary to build our Airflow image. Open a terminal, navigate to the place where you usually store your code, and run the following command to make a new project directory and cd into it:

```
mkdir astronomer-trial && cd astronomer-trail
```

Once you're in that project directory, run:

```
 astro airflow init
```

This will generate some skeleton files:

```py
.
├── dags #Where your DAGs go
│   ├── example-dag.py ##An example dag that comes with the initialized project.
├── Dockerfile #For runtime overrides
├── include #For any other files you'd like to include
├── packages.txt #For OS-level packages
├── plugins #For any custom or community Airflow plugins
└── requirements.txt #For any python packages
```

Note that running this command generates an example DAG for you to deploy while getting started. This DAG doesn't have much functionality (it just prints the date a bunch of times), as it's designed to help you get accustomed with our deployment flow. If you'd like to deploy some more functional example DAGs, [check out the one's we've open sourced here](https://github.com/airflow-plugins/example-dags).

### Customize Your Image

Our base image runs Alpine Linux, so it is very slim by default.

- Add DAGs in the `dags` directory
- Add custom airflow plugins in the `plugins` directory
- Python packages can go in `requirements.txt`. By default, you get all the python packages required to run airflow.
- OS level packages  can go in `packages.txt`
- Any environment variable overrides can go in `Dockerfile` (_note_: with Astronomer 0.7, you can also inject env vars directly through the UI)

If you are unfamiliar with Alpine Linux, look here for some examples of what
you will need to add based on your use-case:

- [GCP](https://github.com/astronomer/airflow-guides/tree/master/example_code/gcp/example_code)
- [Snowflake](https://github.com/astronomer/airflow-guides/tree/master/example_code/snowflake/example_code)
- More coming soon!

### Run Apache Airflow Locally

Before you're ready to deploy your DAGs, you'll want to make sure that everything runs locally as expected.

If you've made sure everything you need to your image is set, you can run:

```bash
astro airflow start
```

This will spin up a local Airflow for you to develop on that includes locally running docker containers - one for the Airflow Scheduler, one for the Webserver, and one for postgres (Airflow's underlying database).

To verify, you can run: `docker ps`

The Airflow UI doesn't always show the full stacktrace. To get some more information while you're developing locally, you can run:

```bash
docker logs $(docker ps | grep scheduler | awk '{print $1}')
```

**Note on Python Versioning:** Astronomer Cloud runs Python 3.6.6. If you're running a different version, don't sweat it. Our CLI spins up a containerized environment, so you don't need to change anything on your machine if you don't want to.

## Start a Trial with Astronomer

To sign up for a free trial on Astronomer, fill out [this form](https://trial.astronomer.io). If you have an issue providing credit card information right off the bat, [contact us](https://www.astronomer.io/contact/?from=/).

## Create a Workspace

Once you've kicked off your trial, you'll be directed to create an account on Astronomer. You can auth in via Google, Github, or standard username/password authentication. Note that once your account is created, you won't be able to change your method of authorization.

Your account will be equipped with a personal Workspace by default. You can think of your Workspaces the same way you'd think of teams - they're collections of Airflow deployments that specific user groups have access to.  Airflow deployments are hierarchically lower - from a workspace, you can create one or more Airflow deployments.

### Join another Workspace

If you're new to Astronomer but someone else on your team has an existing workspace you want to join, you'll still need to [create an account](https://app.astronomer.cloud/signup). A personal workspace for you will be generated regardless, and that team member will be able to add you as a user to a shared workspace directly from their account*.

Read more about Astronomer's UI [here](https://www.astronomer.io/docs/airflow-deployments/).

*If you have any trouble with the confirmation email, feel free to reach out. It's usually becuase of network security settings, so check your spam folder and try to whitelist our domain if you can.

## Create an Airflow Deployment

If you already have a deployment created in your Astronomer Workspace, you can skip this step. If not, go ahead and create a deployment directly from our app by following the steps below:

- Start from https://app.astronomer.cloud/workspaces
- Click into the workspace you want to create a deployment from
- Hit `New Deployment` on the top right of the page
- Give your deployment a name and description
- Wait a few minutes (might have to refresh) for your webserver, scheduler, and celery flower (worker monitoring) to spin up

Once you see an active URL under “Apache Airflow” in the middle of the page, you are set and ready to deploy your DAGs.

<!-- **Note**: For abstraction from the Astro UI, you can also create a deployment [via the CLI](https://www.astronomer.io/docs/cli-getting-started/). -->

## Deploy your First DAG

Once everything is up and running locally, you're ready to deploy your first DAG.

### Step 1: Login

To log into your existing account and pass our authorization flow, run the following command:

```
astro auth login astronomer.cloud
```

You _can_ login via app.astronomer.cloud directly but our UI currently does not display the workspace ID you'll need to complete a deployment.

### Step 2: Make sure you're in the right place

To get ready for deployment, make sure:

- You're logged in
- You're in the right workspace
- Your target deployment lives under that workspace

Follow our [CLI Getting Started Guide](https://www.astronomer.io/docs/cli-getting-started/) for more specific guidelines and commands.

### Step 3: Deploy

When you're ready to deploy your DAGs, run:

  `astro airflow deploy`

This command will return a list of deployments available in that workspace, and prompt you to pick one.

### Step 4: View your Example DAG on your Astronomer Cluster

After you deploy your example DAG, you'll be able to see it running in your Cloud deployment.

**Note:** If you're interested in using Cloud for your production workflows, you're all set! If you followed this guide as a trial but would like to host our platform on your Kubernetes cluster via [Astronomer Enterprise](https://astronomer.io/enterprise), please reach out to us [via this form](https://www.astronomer.io/#request) so we can get a conversation set up.

## Additional Notes

### Migrating your DAGs

If you're a previous user of Astronomer Cloud or have a pre-existing Airflow instance, migrating your DAGs should be straightforward.

For the sake of not over-exposing data and credentials, there's no current functionality that allows you to automatically port over connections and variables from a prior Apache Airflow instance. You'll have to do this manually as you complete the migration.

### Frequently Asked Questions

Check out our [community forum](https://forum.astronomer.io) for FAQs and community discussion.
