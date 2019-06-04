---
title: "Pulling Postgres Credentials"
description: "How to access the username and password you'll need to access a deployment's underlying Postgres Database"
date: 2018-08-24T00:00:00.000Z
slug: "ee-administration-postgres-creds"
---

## Overview

If you're an Enterprise Customer looking to pull the Postgres credentials you need to access an Airflow's deployment's underlying database on your Kubernetes Cluster, follow the guidelines below.

### Pre-Requisites

- Access to your Kubernetes Cluster with permissions to list pods + namespaces
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

**Note**: The example below is based on access to Google's Kubernetes Engine on GCP, but the process should be parallel for other Kubernetes Services.

## How To Pull Postgres Credentials via Kubectl

**1. Switch into your Kubernetes Cluster**

At Astronomer, most of us use [kubectx](https://github.com/ahmetb/kubectx) - a command line tool that allows you to easily switch between clusters and namespaces via kubectl.

**2. List the Namespaces in your Cluster**

For each Airflow deployment in your Cluster, you should see a corresponding namespace.

To list them, run:

```
kubens
```

**3. Enter the Corresponding Namespace**

Find the Kubernetes Namespace that corresponds to the Airflow deployment whose database you'd like credentials to.

```
kubens astronomer-cloud-quasaric-sun-9051
```

You should see the following components appear:

```
Paolas-MacBook-Pro:hello-astro paola$ kubectl get pods
NAME                                                    READY   STATUS    RESTARTS   AGE
quasaric-sun-9051-flower-7bbdf98d94-zxxjd      1/1     Running   0          93d
quasaric-sun-9051-2346-pgbouncer-c997bbd9d-dgsjr    2/2     Running   0          2d
quasaric-sun-9051-2346-redis-0                      1/1     Running   0          93d
quasaric-sun-9051-2346-scheduler-59f856bd5-d7gl4    1/1     Running   0          3h
quasaric-sun-9051-2346-statsd-5c7d7b6777-x7v4x      1/1     Running   0          93d
quasaric-sun-9051-2346-webserver-56fb447559-gjg8n   1/1     Running   0          3h
quasaric-sun-9051-2346-worker-0
```

**4. Describe Scheduler Pod**

```
kubectl describe pod <SCHEDULER POD NAME>
```

**5. Get Secret**

Run:

```
kubectl get secret
```

Then:

```
kubectl get secret <insert airflow metadata pod>
```

Then:

```
echo
```

**6. Copy Credentials**

You'll get something like the following as output (don't worry, this is a sample deployment):

```
Paolas-MacBook-Pro:hello-astro paola$ echo "cG9zdGdyZXNxbDovL2dlb2NlbnRyaWNfaW5zdHJ1bWVudF8yMzQ2X2FpcmZsb3c6VTJvN3F2VnVsWnZ5cXl2V1hXbTBSSGh1UHlqdk1IT3BAZ2VvY2VudHJpYy1pbnN0cnVtZW50LTIzNDYtcGdib3VuY2VyOjY1NDMvZ2VvY2VudHJpYy1pbnN0cnVtZW50LTIzNDYtbWV0YWRhdGE=" | base64 --decode
postgresql://quasaric_sun_9051_airflow:U2o7qvVulGvyqyvAXWm0RPhuPvjvlHOp@geocentric-instrument-2346-pgbouncer:6543/geocentric-instrument-2346-metadataPaolas-MacBook-Pro:hello-astro paola$ 
```

The credentials you're looking for are in between `postgresql://` and the `@` in the following format:

Username: quasaric_sun_9051_airflow
Password: U2o7qvVulGvyqyvAXWm0RPhuPvjvlHOp

And you're set! To finish connecting to this deployment's Postgres, go back to [our doc on querying the Airflow database](https://astronomer.io/docs/query-airflow-database/).






















