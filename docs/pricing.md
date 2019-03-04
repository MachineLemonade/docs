---
title: "Pricing"
description: "Documentation of our pricing structure and philosophy."
date: 2018-10-12T00:00:00.000Z
slug: "pricing"
---

To view a general overview of our pricing structure, check out the [pricing page](https://www.astronomer.io/pricing/) on our website.

## Cloud Pricing

### Overview

As part of our promise to give our customers more freedom and control with Apache Airflow, Astronomer Cloud is priced based on exact resource usage per deployment. Your monthly charge is based on the total number of Airflow deployments tied to your organization and the total AU hours you allocate to each of those instances.

Our Cloud platform is fully managed on Astronomer's infrastructure, allowing you to run as many deployments (and DAGs) as you'd like. Each of your deployments is powered by an isolated set of resources that can be scaled up or down to fit your needs and the architecture of your running workflows.

Resource configuration is directly managed on the `Configure` tab of the Astronomer UI (check out our [Astronomer UI Guide](https://www.astronomer.io/docs/airflow-deployments/) for more detail).

### Configuration Overview

For us to maximize your control over your Airflow deployments, our monthly cost to run Astronomer Cloud fully depends on how much you scale each component of your Airflow instance(s) - and for how long - throughout the course of your billing cycle.

Via the [Astronomer UI](https://app.astronomer.cloud/login), you can freely scale the following components of each of your instances:

- Webserver
- Scheduler
- Celery worker count
- Celery worker size
- Celery worker termination grace period

Resource configurations are "live" as soon as you adjust the toggles on your web browser and click `Update`.

### The Astronomer Unit (AU)

To track and measure allocation to each of these components, we introduce the concept of an Astronomer Unit (AU).

| AU Count | CPU | GB of Memory | Monthly Price |
|----------|-----|--------|-------|
| 1 | 0.1 | .375 | $10 |
| 10 | 1 | 3.75 | $100


When you spin up an Airflow deployment, you'll find that it's pre-configured with default resource allocations. We've identified those levels to be effective baselines for the Local and Celery executors ,respectively. Of course, you're free to adjust them freely at any time.

See below for out-of-the-box configurations and corresponding AU count:

| Executor | PgBouncer & StatsD | Scheduler | Webserver | Celery Worker | Redis & Flower | Total AU | Total Monthly Cost |
|----------|-----|--------|-------|
| Local | 4 | 5 | 2 | N/A | N/A | 11 | $110 |
| Celery | 4 | 5 | 2 | 10 | 4 | 25 | $250 |

**Note**: The PgBouncer, StatsD, Redis, and Flower AU configs are static infrastructure minimums that cannot be changed.

One Celery worker, for example, is powered by 1 AU by default but can be modified at any time.

#### Billing

To calculate your bill at the end of the month, we take a snapshot of your deployment's resource allocations every individual hour your deployment is running on our platform (via an Airflow DAG, of course).

At the end of the month, we aggregate the total AU hours for that billing cycle - and convert it to a dollar amount.

For example, the cost of running 1 deployment on 25 AUs (a standard deployment with 1 worker using the Celery executor) for 1 day = (25) x (0.0137) x (24).

**Note**: Scheduled downtime is not currently supported. Check out a [related forum question](https://forum.astronomer.io/t/can-i-have-scheduled-downtime/35) for more info.

## Enterprise Pricing

Astronomer Enterprise is priced via an annual licensing fee. You'll get access to the entire source code that powers Astronomer and pay us a flat fee for unlimited workers and Airflow deployments on your Kubernetes cluster.

For a breakdown of the components that come with that license, check out our [Platform Overview](https://www.astronomer.io/docs/overview/) page.

If you're interested in Enterprise and haven't already talked to us, reach out to start a trial [here](https://www.astronomer.io/enterprise/#request).
