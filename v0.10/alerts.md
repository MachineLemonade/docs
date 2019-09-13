---
title: "Built-in Alerts"
description: "A guide to Astronomer's built in alerting systems."
date: 2018-10-12T00:00:00.000Z
slug: "alerts"
---

Get emails for common Airflow deployment and platform issues.

Alerts are defined in Helm, and use the [PromQL query language](https://prometheus.io/docs/prometheus/latest/querying/basics/).

## Airflow Alerts

> Note: view [full source code](https://github.com/astronomer/helm.astronomer.io/blob/master/charts/prometheus/values.yaml) for these alerts.

| Alert | Description |
| ------------- | ------------- |
| `AirflowDeploymentUnhealthy` | Release deployment is unhealthy, not completely available. |
| `AirflowFailureRate` | Airflow tasks are failing at a higher rate than normal. |
| `AirflowSchedulerUnhealthy` | Airflow scheduler is unhealthy, heartbeat has dropped below the acceptable rate. |
| `AirflowPodQuota` | Deployment is near its pod quota, has been using over 95% of it's pod quota for over 10 minutes. |
| `AirflowCPUQuota` | Deployment is near its CPU quota, has been using over 95% of it's CPU quota for over 10 minutes. |
| `AirflowMemoryQuota` | Deployment is near its memory quota, has been using over 95% of it's memory quota for over 10 minutes. |

## Platform Alerts

> Note: view [full source code](https://github.com/astronomer/helm.astronomer.io/blob/master/charts/prometheus/templates/prometheus-alerts-configmap.yaml) for these alerts.

| Alert | Description |
| ------------- | ------------- |
| `PrometheusDiskUsage` | Prometheus high disk usage, has less than 10% disk space available. |
| `RegistryDiskUsage` | Docker Registry high disk usage, has less than 10% disk space available. |
| `ElasticsearchDiskUsage` | Elasticsearch high disk usage, has less than 10% disk space available. |
| `IngessCertificateExpiration` | TLS Certificate expiring soon, expiring in less than a week. |
