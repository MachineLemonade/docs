---
title: "Pulling Postgres Credentials"
description: "How to get Credentials to access Metadata for an Airflow Deployment on Astronomer"
date: 2018-08-24T00:00:00.000Z
slug: "ee-administration-postgres-creds"
---

## Overview

Each Airflow deployment on Astronomer maintains a separate metadata database. The credentials for these are stored as Kubernetes secrets within that namespace. To pull the credentials you need to access your deployment's underlying database, follow the guidelines below.

### Pre-Requisites

- Access to your Kubernetes Cluster with permissions to list pods + namespaces
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

## How To Pull Postgres Credentials via Kubectl

**1. Switch into your Kubernetes Cluster**

The rest of this guide will assume use of [kubectx](https://github.com/ahmetb/kubectx) - a command line tool that allows you to easily switch between clusters and namespaces via kubectl.

**2. List the Namespaces in your Cluster**

Each Airflow deployment on Astronomer runs in a separate [Kubernetes Namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/).

To list the namespaces on your cluster, run:

```
kubens
```

**3. Confirm your Deployment's Corresponding Namespace**

Find the Kubernetes Namespace that corresponds to the Airflow deployment whose database you'd like credentials to, and then run.

```
kubens <NAMESPACE>
```

If you run `kubectl get pods` from there, you should see the following components appear:

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

**4. Get Secret**

As a next step, you'll have to pull the Kubernetes secret that lives in your Scheduler pod.

Run:

```
kubectl get secret
```

Then:

```
kubectl get secret <airflow metadata pod>
```

Now, let's decode it:

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

- Username: quasaric_sun_9051_airflow
- Password: U2o7qvVulGvyqyvAXWm0RPhuPvjvlHOp

And you're set! To finish connecting to this deployment's Postgres, go back to [our doc on querying the Airflow database](https://astronomer.io/docs/query-airflow-database/).






















