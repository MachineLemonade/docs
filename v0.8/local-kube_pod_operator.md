---
title: "Running KupePodOperator Locally"
description: "How to set up a local instance of Kubernetes for testing your KubePodOperators"
date: 2019-05-08T00:00:00.000Z
slug: "setting-up-airflow-emails"
---

### Setup Kubernetes
#### Mac
The latest version of Docker for Mac comes with the ability to run a single node Kubernetes cluster on your local machine. You can enable this by going into the Kubernetes section of you docker settings and checking the `Enable Kubernetes` checkbox. Also change the default orchestrator to Kubernetes. Click apply, and the docker service will restart. When it’s back up and running, you should see the green dot in the bottom left hand corner indicating Kubernetes is running. [Docker's docs](https://docs.docker.com/docker-for-mac/#kubernetes)

#### Windows 10 with WSL
Follow [this guide](https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly) for setting up Docker for Windows 10 and WSL. (you don’t need to install docker-compose if you don’t want to)

The latest versions of Docker for Windows comes with the ability to run a single node Kubernetes cluster on your local machine. You can enable this by going into the Kubernetes section of you docker settings and checking the `Enable Kubernetes` checkbox. Also change the default orchestrator to Kubernetes. Click apply, and the docker service will restart. When it’s back up and running, you should see the green dot in the bottom left hand corner indicating Kubernetes is running. [Docker's docs](https://docs.docker.com/docker-for-windows/#kubernetes)

#### Linux
Coming Soon…

### Astronomer
Navigate to an existing Astro project or create a new one in an empty folder with `astro airflow init`. Create a new folder in this directory named `.kube`. Now navigate to your user home directory and look for a folder named `.kube`. It may be hidden. This was created when you enabled Kubernetes in Docker and contains a file named `config`. Copy this file into the `.kube` folder of your Astro project. Now open this file up with a text editor. This file contains all the information the KubePodOperator uses to connect to your cluster. Under cluster, you should see `server: https://localhost:6445`. Change this to `server: https://host.docker.internal:6445`. This way the docker container running airflow knows to look at your machine’s localhost.

**Note:** This file does contain a key to connect to your local Kubernetes cluster, so you may want to add this file to `.gitignore` so it’s not pushed to your git repo.

Airflow
The KubePodOperator is available in Airflow 1.10 or later so make sure your Dockerfile is using a 1.10 image. example `FROM astronomerinc/ap-airflow:0.7.5-1.10.2-onbuild`. Now create a DAG that uses the KubePodOperator like the example below.

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
This example simply runs the docker `hello-world` image. The `config_file` is pointing to the `.kube/config` file you just edited. Now run `astro airflow start` and unpause your DAG. You should see the task run successfully. If you installed `kubectl` above, you can use this to examine the pod that just ran.
