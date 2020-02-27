---
title: "Getting Started with Astronomer Certified Airflow"
description: "Everything you need to know to get up and running on Astronomer's distribution of Apache Airflow"
date: 2020-26-12T00:00:00.000Z
slug: "getting-started-cea"
---

## Overview

Designed in close partnership with both Airflow committers and users, Astronomer Certified Enterprise Airflow (CEA) is for teams ready to leverage the Python-based workflow management tool in production. CEA combines Airflow’s extensibility and community-driven development with industry standards for security, reliability, and scale.

## Get Started with CEA

There are two primary ways to install Astronomer CEA:

1. Docker (`docker run`)
2. Python Package (`pip install`)

CEA currently supports Airflow versions 1.10.5 - 1.10.7. This doc should cover everything you need to know to run Astronomer CEA via either method, including:

- Pre-Requisites
- Instructions for Local Dev
- Instructions for Deploying CEA to Production

## CEA on Docker

The preferred way to install Astronomer CEA is to download our latest Astronomer-hosted Docker image, each of which will generally correspond with an open-source Airflow release.

For Astronomer's full collection of Docker Images, reference our public [Docker Hub repository](https://hub.docker.com/r/astronomerinc/ap-airflow).

### Run Locally

#### Pre-Requisites

To run CEA locally, you'll need the following on your machine:

- Docker
- Docker Compose

The easiest way to install both is to start with [Docker Desktop](https://www.docker.com/products/docker-desktop).

To verify Docker is installed and your user has the right permissions, run:

```
docker run -it --rm hello-world
```

#### Install

Once you're all set on Docker, do the following:

- [Insert Yaml file]
- `docker-compose up`

By default, the above will get you set up on a Local Executor. When you run it, containers for your Airflow Metadata Database, Airflow Webserver and Airflow Scheduler are spun up programmatically (this is the equivalent of running `airflow initdb`, `airflow webserver` and `airflow scheduler`).

### Run in Production

#### Pre-Requisites

In order to install CEA on Docker, make sure you have the following:

- [Docker](https://www.docker.com/)
- Postgres DB
- Redis (if Celery Executor)

#### Deploy

Once you're ready to run CEA, make sure:

- Your DAG files must be available in `/usr/local/airflow/dags` -- either by volume mounting or building them in to the image
- `webserver RBAC = True` (this is the default, setting this to false is an unsupported configuration)
- Set `AIRFLOW__CORE__SQL_ALCHEMY_CONN` Env Var pointing at a Postgres DB (set when you do docker run)

When you're ready to deploy in Production, you'll need to:

- Deploy 1 Docker container for Webserver, 1 for Scheduler (running the same image in a few different ways)
- If you'd like to Celery Executor, you'll need Redis and at least 1 worker container (ask for command - config baked in)
- We recommend you bake your DAGs into your image (when you change your DAGs, push a new image - preferably using CI)

#### Deployment Config

- You'll get empty airflow.cfg file at runtime (not required)
- Env Vars (If it's not environment specific, you can put it into your airflow.cfg if you want to bake it into your image. If things change between instances, set Env Vars (arg when you do docker run))

#### Run on K8s
Docs coming soon...

#### Install

### Install via Python Wheel


