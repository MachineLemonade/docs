---
title: "Customizing Built-in Alerts"
description: "A guide to Astronomer's built-in alerting systems."
date: 2018-10-12T00:00:00.000Z
slug: "alerts"
---

Route common Airflow deployment and platform alerts to your preferred channel, via [Prometheus Alertmanager](https://prometheus.io/docs/alerting/alertmanager).

Alerts are defined using the [PromQL query language](https://prometheus.io/docs/prometheus/latest/querying/basics/).

Alertmanager then manages those alerts, including silencing, inhibition, aggregation and sending out notifications via methods such as email, on-call notification systems, and chat platforms.

You can [configure Alertmanager](https://prometheus.io/docs/alerting/configuration/) to send alerts to email, HipChat, PagerDuty, Pushover, Slack, OpsGenie, and more by editing the [Alertmanager ConfigMap](https://github.com/astronomer/helm.astronomer.io/blob/master/charts/alertmanager/templates/alertmanager-configmap.yaml).

> Note: We are considering a feature to be able to define and customize alerts within the Astronomer UI, but this won't happen until after v1.0.

## Airflow Alerts

You can view [full source code](https://github.com/astronomer/helm.astronomer.io/blob/master/charts/prometheus/values.yaml) for these built-in alerts.

| Alert | Description |
| ------------- | ------------- |
| `AirflowDeploymentUnhealthy` | Release deployment is unhealthy, not completely available. |
| `AirflowFailureRate` | Airflow tasks are failing at a higher rate than normal. |
| `AirflowSchedulerUnhealthy` | Airflow scheduler is unhealthy, heartbeat has dropped below the acceptable rate. You may want to customize this query if it is too noisy by default. |
| `AirflowPodQuota` | Deployment is near its pod quota, has been using over 95% of it's pod quota for over 10 minutes. |
| `AirflowCPUQuota` | Deployment is near its CPU quota, has been using over 95% of it's CPU quota for over 10 minutes. |
| `AirflowMemoryQuota` | Deployment is near its memory quota, has been using over 95% of it's memory quota for over 10 minutes. |

End users can subscribe to these configured alerts in the Astronomer UI.

## Platform Alerts

You can view [full source code](https://github.com/astronomer/helm.astronomer.io/blob/master/charts/prometheus/templates/prometheus-alerts-configmap.yaml) for these built-in alerts.

| Alert | Description |
| ------------- | ------------- |
| `PrometheusDiskUsage` | Prometheus high disk usage, has less than 10% disk space available. |
| `RegistryDiskUsage` | Docker Registry high disk usage, has less than 10% disk space available. |
| `ElasticsearchDiskUsage` | Elasticsearch high disk usage, has less than 10% disk space available. |
| `IngessCertificateExpiration` | TLS Certificate expiring soon, expiring in less than a week. |

Admins can subscribe to these configured alerts bt editing the [Alertmanager ConfigMap](https://github.com/astronomer/helm.astronomer.io/blob/master/charts/alertmanager/templates/alertmanager-configmap.yaml).

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
