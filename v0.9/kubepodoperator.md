---
title: "KubernetesPodOperator on Astronomer"
description: "How to run the KubernetesPodOperator on Astronomer"
date: 2019-04-29T00:00:00.000Z
slug: "kubepodoperator"
---

The [KubernetesPodOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/kubernetes_pod_operator.py) allows you to natively launch Kubernetes Pods in which to run a Docker container, all using the [Kube Python Client](https://github.com/kubernetes-client/python) to generate a Kubernetes API request. This allows Airflow to act as an orchestrator of your jobs, no matter the language they're written in.

### Description

The KubePodOperator works the same way as the Docker Operator - all you need to do is supply a Docker image to run. Astronomer Cloud is a multi-tenant install of Astronomer Enterprise that sits on top of Google's Kubernetes Engine (GKE). As a Cloud customer, you do NOT need to provide the Kubernetes overhead. We'll take care of that for you. If you are Enterprise customer, everything is configured to run when you deploy the platform.

Note: The Docker Operator is NOT supported on Astronomer for security reasons (we'd have to expose the Docker socket through to containers with a mount and let an unmanaged container run on the host machine).

### Usage on Astronomer

#### Make sure you are running Astronomer Airflow 1.10.x
   - If you're running Airflow 1.9, check out [this forum post](https://forum.astronomer.io/t/how-do-i-run-airflow-1-10-on-astronomer-v0-7/58) to upgrade.


#### Specify Parameters
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
    in_cluster=True,
    task_id="task-two",
    get_logs=True)
```

- For Astronomer Cloud, your namespace on Kubernetes will be `astronomer-cloud-deployment_name` (e.g. `astronomer-cloud-frigid-vacuum-0996`)
    - For Astronomer Enterprise, this would be be your `base-namespace-deployment` name (e.g. `astronomer-frigid-vacuum-0996`)
- Set the `in_cluster` parameter to `True` in your code
    - This will tell your task to look inside the cluster for the Kubernetes config. In this setup, the workers are tied to a role with the right privileges in the cluster.

#### Add Resources to your Deployment on Astronomer

The KubernetesPodOperator will launch pods on resources allocated to it in the `Extra Capacity` section of your deployment's `Configure` page of the [Astronomer UI](https://www.astronomer.io/docs/astronomer-ui/). Pods will **only** run on the resources configured here. The rest of your deployment will run on standard resources.

For `Extra Capacity`, we recommend starting with **10AU**, and scaling up from there as needed. If it's set to 0, you'll get a permissions error:

```
ERROR - Exception when attempting to create Namespaced Pod.
Reason: Forbidden
"Failure","message":"pods is forbidden: User \"system:serviceaccount:astronomer-cloud-solar-orbit-4143:solar-orbit-4143-worker-serviceaccount\" cannot create pods in the namespace \"datarouter\"","reason":"Forbidden","details":{"kind":"pods"},"code":403}
```

On Astronomer Cloud, the largest node a single pod can occupy is `13.01GB` and `3.92 CPU`. We'll be introducing larger options in Astronomer v0.9, so stay tuned.

On Enterprise, it will depend on the size of your underlying node pool.

### Pulling from a Private Registry

By default, the KubePodOperator will look for images hosted publicly on [Dockerhub](https://hub.docker.com/). If you want to pull from a private registry, you'll have to create a `dockerconfigjson` using your existing Docker credentials.
If you're an Astronomer Cloud customer, [reach out to us](support@astronomer.io) and we can get this secret added for you.

For Enterprise customers, follow the [official Kubernetes](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#registry-secret-existing-credentials) doc to add that secret to the right namespace.

**Note:** The KubernetesPodOperator doesn't support passing in image pull secrets until [Airflow 1.10.2](https://github.com/apache/airflow/blob/master/CHANGELOG.txt#L526).


### Local Testing

Follow our [CLI doc](https://github.com/astronomer/docs/blob/master/v0.8/cli-kubepodoperator.md) on using [Microk8s](https://microk8s.io/) or [Docker for Kubernetes](https://matthewpalmer.net/kubernetes-app-developer/articles/how-to-run-local-kubernetes-docker-for-mac.html).
