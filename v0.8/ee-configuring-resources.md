---
title: "Configuring Resources with Helm"
description: "Change your platform's default resources"
date: 2018-07-17T00:00:00.000Z
slug: "ee-configuring-resources"
---

# Default Resources

By default, Astronomer needs around 10 CPUs and 44Gi of memory:

| Pod                        | Request CPU  | Request Mem  | Limit CPU  | Limit Mem  | Storage |
|-------------------------|--------------|---|---|---|---|
| `orbit`                 | 100m         | 256Mi  | 500m  | 1024Mi  | NA |
| `houston`               | 250m         | 512Mi  | 800m  | 1024Mi  | NA |
| `prisma`                | 250m         | 512Mi  | 500m  | 1024Mi  | NA |
| `commander`             | 250m         | 512Mi  | 500m  | 1024Mi  | NA |
| `registry`              | 250m         | 512Mi  | 500m  | 1024Mi  | 100Gi |
| `install`               | 100m         | 256Mi  | 500m  | 1024Mi  | NA |
| `nginx`                 | 500m         | 1024Mi  | 1  | 2048Mi  | NA |
| `grafana`               | 250m         | 512Mi  | 500m  | 1024Mi  | NA |
| `prometheus`            | 1000m        | 4Gi  | 1000m  | 4Gi  | 100Gi |
| `elasticsearch client replica-1`  | 1            | 2Gi  | 2  | 4Gi  | NA |
| `elasticsearch client replica-2`  | 1            | 2Gi  | 2  | 4Gi  | NA |
| `elasticsearch data replica-1`    | 1            | 2Gi  | 2  | 4Gi  | 100Gi |
| `elasticsearch data replica-2`    | 1            | 2Gi  | 2  | 4Gi  | 100Gi |
| `elasticsearch master replica-1`  | 1            | 2Gi  | 2  | 4Gi  | 20Gi|
| `elasticsearch master replica-2`  | 1            | 2Gi  | 2  | 4Gi  | 20Gi|
| `elasticsearch master replica-3`  | 1            | 2Gi  | 2  | 4Gi  | 20Gi|
| `kibana`                | 250m         | 512Mi  | 500m  | 1024Mi  | NA |
| `fluentd`               | 250m         | 512Mi  | 500m  | 1024Mi  | NA |
| `kubeState`             | 250m         | 512Mi  | 500m  | 1024Mi  | NA |
| Total                   | 10.7          | 23.5Gi  | 21.3  | 44Gi  | 460Gi |

## Changing Values

You can change the request and limit of any of the components above in your `config.yaml` or in `values.yaml` (`config.yaml` will overwrite `values.yaml`).

To change something like the resources allocated to `Orbit`, add
```
#####
#Changing Orbit CPU
####

astronomer:
  orbit:
    resources:
      requests:
        cpu: "200m"
        memory: "256Mi"
      limits:
        cpu: "700m"
        memory: "1024Mi"
```
to `config.yaml`

Once all the changes are made, run `helm upgrade` to switch your platform to the new config:

```
helm upgrade -f config.yaml $release_name . --namespace $namespace
```
Be sure to specify the platform namespace, not an Airflow namespace.
