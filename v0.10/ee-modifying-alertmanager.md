---
title: "Modifying Alertmanager"
description: "Sending Alerts to external sources"
date: 2018-10-12T00:00:00.000Z
slug: "ee-modifying-alertmanager"
---

## Alertmanager

Astronomer users [Alertmanager](https://prometheus.io/docs/alerting/alertmanager/) to push platform level alerts from Prometheus. Currently, these alerts can be subscribed to by email in the UI. The alertmanager `alert-manager-configmap.yaml` file can be modified to push alerts to external sources.


### Sending Alerts to Slack
To add Slack as a destination for platform alerts, navigate to `helm.astronomer.io/charts/alertmanager/templates/alertmanager-configmap.yaml` and add the necessary configurations to for a Slack channel:

```
################################
## Alertmanager ConfigMap
#################################
kind: ConfigMap
apiVersion: v1
metadata:
  name: {{ template "alertmanager.fullname" . }}
  labels:
    tier: monitoring
    component: {{ template "alertmanager.name" . }}
    chart: {{ template "alertmanager.chart" . }}
    release: {{ .Release.Name }}
    heritage: {{ .Release.Service }}
data:
  alertmanager.yaml: |-
    route:
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 3h
  receiver: default-receiver
  routes:
  - receiver:  blackhole-receiver
    match_re:
      tier: platform
  - receiver:  default-receiver
    group_by: [deployment, alertname]
    match_re:
      tier: airflow
receivers:
- name: platform-receiver
  slack_configs:
  - channel: '<channel>'
    api_url: <url>
    title:  "{{ .CommonAnnotations.Name }}"
    text: |-
      {{ range .Alerts }}
        *Alert:* {{ .Annotations.summary }}
        *Description:* {{ .Annotations.description }}
        *Details:*
        {{ range .Labels.SortedPairs }} • *{{ .Name }}:* {{ .Value }}
        {{ end }}
      {{ end }}
- name: airflow-receiver
  slack_configs:
  - channel: '<channel>'
    api_url: <url>
    title:  "{{ .CommonAnnotations.Name }}"
    text: |-
      {{ range .Alerts }}
        *Alert:* {{ .Annotations.summary }}
        *Description:* {{ .Annotations.description }}
        *Details:*
        {{ range .Labels.SortedPairs }} • *{{ .Name }}:* {{ .Value }}
        {{ end }}
      {{ end }}
- name: blackhole-receiver
# Deliberately left empty to not deliver anywhere.
- name: default-receiver
  webhook_configs:
  - url: http://astronomer-houston:8871/v1/alerts
    send_resolved: true
```

Substitute the appropriate values for the channel and api_url and save the file.


## Deploying the change

Now that the `alertmanager-configmap.yaml` has been updated, the change can be pushed to the Astronomer Deployment.

```
$ helm ls
NAME         	REVISION	UPDATED                 	STATUS  	CHART                           	APP VERSION	NAMESPACE 
astronomer 	1       	Tue Dec  3 21:11:49 2019	DEPLOYED	astronomer-platform-0.10.3-fix.3	0.10.3     	astronomer

$ helm upgrade astronomer -f config.yaml . --namespace astronomer
```