---
title: "KubernetesPodOperator on Astronomer"
description: "How to run the KubernetesPodOperator on Astronomer"
date: 2019-04-29T00:00:00.000Z
slug: "kubepodoperator"
---

The [KubernetesPodOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/kubernetes_pod_operator.py) allows you to natively launch Kubernetes Pods in which to run a Docker container, all using the [Kube Python Client](https://github.com/kubernetes-client/python) to generate a Kubernetes API request. This allows Airflow to act as an orchestrator of your jobs, no matter the language they're written in.

## Description

The KubePodOperator works the same way as the Docker Operator - all you need to do is supply a Docker image to run. Astronomer Cloud is a multi-tenant install of Astronomer Enterprise that sits on top of Google's Kubernetes Engine (GKE). As a Cloud customer, you do NOT need to provide the Kubernetes overhead. We'll take care of that for you. If you are Enterprise customer, everything is configured to run when you deploy the platform.

Note: The Docker Operator is NOT supported on Astronomer for security reasons (we'd have to expose the Docker socket through to containers with a mount and let an unmanaged container run on the host machine).

## Usage on Astronomer

### Make sure you are running Astronomer Airflow 1.10.x

If you're running Airflow 1.9, check out [this forum post](https://forum.astronomer.io/t/how-do-i-run-airflow-1-10-on-astronomer-v0-7/58) to upgrade.

### Specify Parameters

You can import the Operator as you would any other plugin in [its GitHub Contrib Folder](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/kubernetes_pod_operator.py)

```python
from airflow.contrib.operators.kubernetes_pod_operator import kubernetes_pod_operator
```

Instantiate the operator based on your image and setup:

```python
k = kubernetes_pod_operator.KubernetesPodOperator(
    namespace='astronomer-cloud-frigid-vacuum-0996',
    image="ubuntu:16.04",
    cmds=["bash", "-cx"],
    arguments=["echo", "10", "echo pwd"],
    labels={"foo": "bar"},
    name="airflow-test-pod",
    is_delete_pod_operator=True,
    in_cluster=True,
    task_id="task-two",
    get_logs=True)
```

The KubePodOperator needs to know which namespace to run in and where to look for the config file.
For Astronomer Cloud, your namespace on Kubernetes will be `astronomer-cloud-deployment_name` (e.g. `astronomer-cloud-frigid-vacuum-0996`)
For Astronomer Enterprise, this would be be your `base-namespace-deployment` name (e.g. `astronomer-frigid-vacuum-0996`)

Set the `in_cluster` parameter to `True` in your code. This will tell your task to look inside the cluster for the Kubernetes config. In this setup, the workers are tied to a role with the right privileges in the cluster.

Set the `is_delete_pod_operator` parameter to `True` in your code. This will delete completed pod in the namespace as they finish, keeping Airflow below its resource quotas.

These parameters can be automatically set with environment variabless (see below).

#### Add Resources to your Deployment on Astronomer

The KubernetesPodOperator will launch pods on resources allocated to it in the `Extra Capacity` section of your deployment's `Configure` page of the [Astronomer UI](https://www.astronomer.io/docs/astronomer-ui/). Pods will **only** run on the resources configured here. Adding `Extra Capacity` will increase your namespace's [resource quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/) so that Airflow has permissions to launch pods in the namespace.

For `Extra Capacity`, we recommend starting with **10AU**, and scaling up from there as needed. If it's set to 0, you'll get a permissions error:

```
ERROR - Exception when attempting to create Namespace Pod.
Reason: Forbidden
"Failure","message":"pods is forbidden: User \"system:serviceaccount:astronomer-cloud-solar-orbit-4143:solar-orbit-4143-worker-serviceaccount\" cannot create pods in the namespace \"datarouter\"","reason":"Forbidden","details":{"kind":"pods"},"code":403}
```

On Astronomer Cloud, the largest node a single pod can occupy is `13.01GB` and `3.92 CPU`. We'll be introducing larger options in future releases, so stay tuned. On Enterprise, it will depend on the size of your underlying node pool.

> Note: If you need your [limit range](https://kubernetes.io/docs/concepts/policy/limit-range/) increased, please contact your system admin if you are an Enterprise customer (or Astronomer if you are a Cloud customer).

#### Define Resources per Task

A notable advantage of leveraging Airflow's KubernetesPodOperator is that you can specify compute [resources](https://github.com/apache/airflow/blob/master/airflow/contrib/operators/kubernetes_pod_operator.py#L85) in the task definition.

```
    :param resources: A dict containing resources requests and limits.
        Possible keys are request_memory, request_cpu, limit_memory, limit_cpu,
        and limit_gpu, which will be used to generate airflow.kubernetes.pod.Resources.
        See also kubernetes.io/docs/concepts/configuration/manage-compute-resources-container
    :type resources: dict
```

#### Example Task Definition:

```
from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow import configuration as conf

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

namespace = conf.get('kubernetes', 'NAMESPACE')

# This will detect the default namespace locally and read the 
# environment namespace when deployed to Astronomer.
if namespace =='default':
    config_file = '/usr/local/airflow/include/.kube/config'
    in_cluster=False
else:
    in_cluster=True
    config_file=None

dag = DAG('example_kubernetes_pod',
          schedule_interval='@once',
          default_args=default_args)


compute_resource = {'request_cpu': '800m', 'request_memory': '3Gi', 'limit_cpu': '800m', 'limit_memory': '3Gi'}

with dag:
    k = KubernetesPodOperator(
        namespace=namespace,
        image="hello-world",
        labels={"foo": "bar"},
        name="airflow-test-pod",
        task_id="task-one",
        in_cluster=in_cluster # if set to true, will look in the cluster, if false, looks for file
        cluster_context='docker-for-desktop', # is ignored when in_cluster is set to True
        config_file=config_file,
        resources=compute_resource,
        is_delete_pod_operator=True,
        get_logs=True)
```

This will launch a pod that runs the `hello-world` image pulled from Dockerhub in whatever namespace the pod is launched with the specified resource request and delete the pod once it finishes running.

## Using a Private Registry

By default, the KubePodOperator will look for images hosted publicly on [Dockerhub](https://hub.docker.com/). If you want to pull from a private registry, you'll have to create a `dockerconfigjson` using your existing Docker credentials.
If you're an Astronomer Cloud customer, [reach out to us](support@astronomer.io) and we can get this secret added for you.

For Enterprise customers, follow the [official Kubernetes](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#registry-secret-existing-credentials) doc to add that secret to the right namespace.

> Note: The KubernetesPodOperator doesn't support passing in image pull secrets until [Airflow 1.10.2](https://github.com/apache/airflow/blob/master/CHANGELOG.txt#L526).

## Local Testing

Follow our [CLI doc](https://www.astronomer.io/docs/cli-kubepodoperator/) on using [Microk8s](https://microk8s.io/) or [Docker for Kubernetes](https://matthewpalmer.net/kubernetes-app-developer/articles/how-to-run-local-kubernetes-docker-for-mac.html) to run tasks with the KubernetesPodOperator locally.
