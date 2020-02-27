---
title: "Cloud Pricing"
description: "Documentation of our pricing structure and philosophy."
date: 2018-10-12T00:00:00.000Z
slug: "pricing"
---

To view a general overview of our pricing structure across our product offerings, check out the [pricing page](https://www.astronomer.io/pricing/) on our website.

### Overview

As part of our promise to give our customers more freedom and control with Apache Airflow, Astronomer Cloud is priced based on exact resource usage per deployment. Your monthly charge is based on the total number of Airflow deployments tied to your organization and the total AU hours you allocate to each of those instances.

Our Cloud platform is fully managed on Astronomer's infrastructure, allowing you to run as many deployments (and DAGs) as you'd like. Each of your deployments is powered by an isolated set of resources that can be scaled up or down to fit your needs and the architecture of your running workflows.

Resource configuration is directly managed on the `Configure` tab of the Astronomer UI (check out our [Astronomer UI Guide](https://www.astronomer.io/docs/airflow-deployments/) for more detail).

### Configuration Overview

For us to maximize your control over your Airflow deployments, our monthly cost to run Astronomer Cloud fully depends on how much you scale each component of your Airflow instance(s) - and for how long - throughout the course of your billing cycle.

Via the [Astronomer UI](https://app.astronomer.cloud/login) as seen below, you can freely scale the following components of each of your instances:

- Webserver
- Scheduler
- Celery worker count
- Celery worker size
- Celery worker termination grace period

![Astro UI Executor Config](https://assets2.astronomer.io/main/docs/astronomer-ui/Astro-UI-Executor.png)

Resource configurations are "live" as soon as you adjust the toggles on your web browser and click `Update`.

### The Astronomer Unit (AU)

To track and measure allocation to each of these components, we introduce the concept of [an Astronomer Unit (AU)](https://github.com/astronomer/houston-api/blob/193183be40df7e00261c3bf4941caf80e5d874a4/config/default.yaml#L317).

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

### Kubernetes Executor

#### Extra Capacity

On Astronomer v0.7 - v0.9, resources needed for either the [KubernetesPodOperator](https://www.astronomer.io/docs/kubepodoperator/) or the KubernetesExecutor are mapped to the `Extra Capacity` slider on your deployment's "Configure" page.

The number of AUs (as a combination of CPU and Memory) maps to [*resource quotas*](https://kubernetes.io/docs/concepts/policy/resource-quotas/) on the [Kubernetes Namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) in which your Airflow deployment lives.

These resources, constrained by said quotas, power any Kubernetes Pod created by implementing either the KubernetesPodOperator or the Kubernetes Executor in your code.

#### Node Limits on Astronomer Cloud

On Astronomer Cloud v0.7.5, the node limits for any single task (based on Google's [standard-4 machine type](https://cloud.google.com/compute/docs/machine-types)) are:

- 13.01 GB of Memory/RAM
- 3.92 CPU

On Astronomer Cloud v0.9, the node limits for any single task (based on Google's [standard-16 machine type](https://cloud.google.com/compute/docs/machine-types)) are:

- 58 GB of Memory/RAM
- 15 CPU

#### Pricing

Astronomer v0.9 introduces the KubernetesExecutor as an alpha feature that does not dynamically "scale to zero" (yet).

Any AU's allocated in the `Extra Capacity` slider will be aggregated *in addition to* resources otherwise allocated to your Scheduler, Webserver, and Workers. If you're an Astronomer Cloud customer, they'll be added to your monthly resource bill at our standard rate of $10/AU.

We'll be making a dynamically scaling KubernetesExecutor a reality on Astronomer in coming releases. Stay tuned.

### Billing

To calculate your bill at the end of the month, we take a snapshot of your deployment's resource allocations every individual hour your deployment is running on our platform (via an Airflow DAG, of course).

At the end of the month, we aggregate the total AU hours for that billing cycle - and convert it to a dollar amount.

For example, the cost of running 1 deployment on 25 AUs (a standard deployment with 1 worker using the Celery executor) for 1 day = (25) x (0.0137) x (24).

**Note**: Scheduled downtime is not currently supported. Check out a [related forum question](https://forum.astronomer.io/t/can-i-have-scheduled-downtime/35) for more info.


## Enterprise Pricing

If you're interested in Enterprise and haven't already talked to us, reach out to start a trial [here](https://www.astronomer.io/enterprise/#request).
