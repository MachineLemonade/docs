---
title: "Customizing Built-in Alerts"
description: "A guide to Astronomer's built-in alerting systems."
date: 2018-10-12T00:00:00.000Z
slug: "alerts"
---

## Overview

Route common Airflow deployment and platform alerts to your preferred channel, via [Prometheus Alertmanager](https://prometheus.io/docs/alerting/alertmanager).

Alerts are defined using the [PromQL query language](https://prometheus.io/docs/prometheus/latest/querying/basics/).

## Accessing Prometheus & Alertmanager UI

You can access the Prometheus & Alertmanager UIs that are deployed in the Astronomer platform using Kubectl to port forward. Example:

```
kubectl port-forward svc/cantankerous-gecko-prometheus -n astronomer 9090:9090
```
```
kubectl port-forward svc/cantankerous-gecko-alertmanager -n astronomer 9093:9093
```

Then visit `localhost:9090` or `localhost:9093` on your computer.

## Configuring Alertmanager

Alertmanager's capabilities include silencing, inhibition, aggregation and sending out notifications via methods such as email, on-call notification systems, and chat platforms.

You can [configure Alertmanager](https://prometheus.io/docs/alerting/configuration/) to send alerts to email, HipChat, PagerDuty, Pushover, Slack, OpsGenie, and more by editing the [Alertmanager ConfigMap](https://github.com/astronomer/helm.astronomer.io/blob/master/charts/alertmanager/templates/alertmanager-configmap.yaml). 

You can also configure Alertmanager's `route` block by editing the [Alertmanager ConfigMap](https://github.com/astronomer/helm.astronomer.io/blob/master/charts/alertmanager/templates/alertmanager-configmap.yaml). The `route` block defines values such as `repeat_interval` (the interval at which alert notifications are sent). You can find more information on the `route` block [here](https://prometheus.io/docs/alerting/configuration/#route)

Example `route` definition:
```
# The root route with all parameters, which are inherited by the child
# routes if they are not overwritten.
route:
  receiver: 'default-receiver'
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  group_by: [cluster, alertname]
  # All alerts that do not match the following child routes
  # will remain at the root node and be dispatched to 'default-receiver'.
  routes:
  # All alerts with service=mysql or service=cassandra
  # are dispatched to the database pager.
  - receiver: 'database-pager'
    group_wait: 10s
    match_re:
      service: mysql|cassandra
  # All alerts with the team=frontend label match this sub-route.
  # They are grouped by product and environment rather than cluster
  # and alertname.
  - receiver: 'frontend-pager'
    group_by: [product, environment]
    match:
      team: frontend
```

## Built-in Airflow Alerts

You can view [full source code](https://github.com/astronomer/helm.astronomer.io/blob/master/charts/prometheus/values.yaml) for these built-in alerts.

| Alert | Description |
| ------------- | ------------- |
| `AirflowDeploymentUnhealthy` | Release deployment is unhealthy, not completely available. |
| `AirflowFailureRate` | Airflow tasks are failing at a higher rate than normal. |
| `AirflowSchedulerUnhealthy` | Airflow scheduler is unhealthy, heartbeat has dropped below the acceptable rate. You may want to customize this query if it is too noisy by default. |
| `AirflowPodQuota` | Deployment is near its pod quota, has been using over 95% of it's pod quota for over 10 minutes. |
| `AirflowCPUQuota` | Deployment is near its CPU quota, has been using over 95% of it's CPU quota for over 10 minutes. |
| `AirflowMemoryQuota` | Deployment is near its memory quota, has been using over 95% of it's memory quota for over 10 minutes. |

Example airflow alert definition:
```
- alert: AirflowDeploymentUnhealthy
  expr: sum by (release) (kube_pod_container_status_running{namespace=~".*-.*-.*-[0-9]{4}"}) - count by (release) (kube_pod_container_status_running{namespace=~".*-.*-.*-[0-9]{4}"}) < 0
  for: 15m 
  labels:
    tier: airflow
    component: deployment
    deployment: "{{ $labels.release }}"
  annotations:
    summary: "{{ $labels.release }} deployment is unhealthy"
    description: "The {{ $labels.release }} deployment is not completely available."
```

You can find more information on alert rule definitions [here](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/). End users can subscribe to these configured alerts in the Astronomer UI. 

## Built-in Platform Alerts

You can view [full source code](https://github.com/astronomer/helm.astronomer.io/blob/master/charts/prometheus/templates/prometheus-alerts-configmap.yaml) for these built-in alerts.

| Alert | Description |
| ------------- | ------------- |
| `PrometheusDiskUsage` | Prometheus high disk usage, has less than 10% disk space available. |
| `RegistryDiskUsage` | Docker Registry high disk usage, has less than 10% disk space available. |
| `ElasticsearchDiskUsage` | Elasticsearch high disk usage, has less than 10% disk space available. |
| `IngessCertificateExpiration` | TLS Certificate expiring soon, expiring in less than a week. |

Example platform alert definition:
```
- alert: PrometheusDiskUsage
  expr: (kubelet_volume_stats_available_bytes{persistentvolumeclaim=~"data-{{ template "prometheus.fullname" . }}-.*"} / kubelet_volume_stats_capacity_bytes{persistentvolumeclaim=~"data-{{ template "prometheus.fullname" . }}-.*"} * 100) < 10
  for: 5m
  labels:
    tier: platform
    component: prometheus
  annotations:
    summary: "Prometheus High Disk Usage"
    description: "Prometheus has less than 10% disk space available."

```

You can find more information on alert rule definitions [here](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/).

### Configuring platform alert receivers

Admins can subscribe to these configured alerts by editing the [Alertmanager ConfigMap](https://github.com/astronomer/helm.astronomer.io/blob/master/charts/alertmanager/templates/alertmanager-configmap.yaml).

Example:

```
alertmanager:
  receivers:
    platform:
      slack_configs:
      - api_url: https://hooks.slack.com/services/T02J89GPR/BDBSG6L1W/4Vm7zo542XYgvv3
        channel: '#astronomer_platform_alerts'
        text: |-
          {{ range .Alerts }}{{ .Annotations.description }}
          {{ end }}
        title: '{{ .CommonAnnotations.summary }}'
```

You can read more about configuration options [here](https://prometheus.io/docs/alerting/configuration/).
