---
title: "Running KubePodOperator Locally"
description: "How to set up a local instance of Kubernetes for testing your KubePodOperators"
date: 2019-05-08T00:00:00.000Z
slug: "cli-kubepodoperator"
---

# Testing with the KubernetesPodOperator Locally

## Setup Kubernetes
### Windows and Mac
The latest version of Docker for Windows and Mac comes with the ability to run a single node Kubernetes cluster on your local machine. If you are on Windows, follow [this guide](https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly) for setting up Docker for Windows 10 and WSL. (you don’t need to install docker-compose if you don’t want to).

Go into Docker>Settings>Kubernetes to check the `Enable Kubernetes` checkbox and change the default orchestrator to Kubernetes. Once these changes are applied, the docker service will restart and the green dot in the bottom left hand corner will indicate Kubernetes is running. [Docker's docs](https://docs.docker.com/docker-for-mac/#kubernetes)


### Linux
Install [microk8s](https://microk8s.io/) and run `microk8s.start` to spin up Kubernetes.

## Get your kube config

### Windows and Mac
Navigate to the `$HOME/.kube` that was created when you enabled Kubernetes in Docker and copy the `config` into a `.kube` folder of in your Astro project. This file contains all the information the KubePodOperator uses to connect to your cluster. Under cluster, you should see `server: https://localhost:6445`. Change this to `server: https://host.docker.internal:6445` to tell the docker container running Airflow knows to look at your machine’s localhost to run Kubernetes Pods.

### Linux

In a `.kube` folder in your Astronomer project, create a config file with:

```bash
microk8s.config > config
```

## Run your container
The `config_file` is pointing to the `.kube/config` file you just edited. Run `astro airflow start` to build this config into your image.

```python
from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('example_kubernetes_pod',
          schedule_interval='@once',
          default_args=default_args)

with dag:
    k = KubernetesPodOperator(
        namespace='default',
        image="hello-world",
        labels={"foo": "bar"},
        name="airflow-test-pod",
        task_id="task-one",
        cluster_context='docker-for-desktop',
        config_file='/usr/local/airflow/.kube/config',
        get_logs=True)

```
This example simply runs the docker `hello-world` image.

If you are on Linux, the `cluster_context` will be `microk8s`

## View Kubernetes Logs

### Windows and Mac
You can use `kubectl get pods -n $namespace` and `kubectl logs {pod_name} -n $namespace` to examine the logs for the pod that just ran.

### Linux
Run the same commands as above prefixed with microk8s:
```
microk8s.kubectl get pods -n $namespace`
```
