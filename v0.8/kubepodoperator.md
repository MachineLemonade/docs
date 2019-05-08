---
title: "KubernetesPodOperator on Astronomer"
description: "How to run the KubernetesPodOperator on Astronomer"
date: 2019-04-29T00:00:00.000Z
slug: "kubepod-operator"
---

The [KubernetesPodOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/kubernetes_pod_operator.py) allows you to natively launch arbitrary Kubernetes Pods in which to run a Docker container using the Kube Python Client to generate a Kubernetes API request.

To leverage this component into your Airflow infrastructure on Astronomer Cloud or Enterprise, check out the guidelines below.

### Description

The KubePodOperator works the same way as the Docker Operator - all you need to do is supply a Docker image to run. Astronomer Cloud is a multi-tenant install of Astronomer Enterprise that sits on top of Google's Kubernetes Engine (GKE). As a Cloud customer, you do NOT need to provide the Kubernetes overhead. We'll take care of that for you.

Note: The Docker Operator is NOT supported on Astronomer for security reasons (we'd have to expose the Docker socket through to containers with a mount and let an unmanaged container run on the host machine).

### Requirements

1. Astronomer Airflow 1.10.x
    - If you're running Airflow 1.9, check out [this forum post](https://forum.astronomer.io/t/how-do-i-run-airflow-1-10-on-astronomer-v0-7/58) to upgrade.
2. Have publicly hosted Docker image

### Intial Setup

- You can import the Operator as you would any other plugin in [its GitHub Contrib Folder](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/kubernetes_pod_operator.py)
- For Astronomer Cloud, your namespace on Kubernetes will be astronomer-cloud-release_name (e.g. `astronomer-cloud-frigid-vacuum-0996`)
    - For Astronomer Enterprise, this would be be your base namespace and deployment name (e.g. `astronomer-yourcompany-frigid-vacuum-0996`)
- Set the `in_cluster` parameter to `True` in your code
    - This will tell your task to look inside the cluster for the Kubernetes config. In this setup, the workers are tied to a role with the right privileges in the cluster.
- Scale the `Extra Capacity` slider in your Deployment `Configure` page to 10+ AU (details below)


**Additional Notes**:

- Make sure you properly configure any relevant keys or credentials (e.g. AWS signature keys), to avoid the following error when pushing up your image:
```
ERROR: S3 error: 403 (SignatureDoesNotMatch): The request signature we calculated does not match the signature you provided. Check your key and signing method.\n’
```
- The KubernetesPodOperator doesn't support passing in image pull secrets until [Airflow 1.10.2](https://github.com/apache/airflow/blob/master/CHANGELOG.txt#L526). If you have that parameter in your DAG and get an error, take that into account and upgrade your Airflow version if you can.
- [Apache Airflow Source Code](http://airflow.apache.org/_modules/airflow/contrib/operators/kubernetes_pod_operator.html)xs

###  Extra Capacity Resources

On Astronomer, the KubernetesPodOperator will run on resources allocated to it in the `Extra Capacity` section of your deployment's `Configure` page of the Astronomer UI. That slider will determine how much resources additional Pods on the cluster get allocated. The rest of your deployment will run on standard resources, so do continue to keep and scale those configurations separately.

For `Extra Capacity`, we recommend starting with **10AU**, and scaling up from there as needed. If it's set to 0 when you're getting started, you might get the following error:

```
ERROR - Exception when attempting to create Namespaced Pod.
Reason: Forbidden
"Failure","message":"pods is forbidden: User \"system:serviceaccount:astronomer-cloud-solar-orbit-4143:solar-orbit-4143-worker-serviceaccount\" cannot create pods in the namespace \"datarouter\"","reason":"Forbidden","details":{"kind":"pods"},"code":403}
```

### Example DAG

Looking for an example? Check out the DAG below, and the original source code in the `airflow-plugins` repo [here](https://github.com/airflow-plugins/example_kubernetes_pod/blob/master/dags/kube_pod_test.py).

```
from airflow import DAG
from datetime import datetime, timedelta
from plugins.operators import kubernetes_pod_operator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('example_kubernetes_pod',
          schedule_interval='@once',
          default_args=default_args)

with dag:
    k = kubernetes_pod_operator.KubernetesPodOperator(
        namespace='datarouter',
        image="ubuntu:16.04",
        cmds=["bash", "-cx"],
        arguments=["echo", "10", "echo pwd"],
        labels={"foo": "bar"},
        name="airflow-test-pod",
        in_cluster=True,
        task_id="task-two",
        get_logs=True)
```

### FAQ's

**Is there a resource cap on a KubernetesPod?**

Right now, the largest node a single pod can occupy is `13.01GB` and `3.92 CPU`. We'll be introducing larger options in Astronomer v0.9, so stay tuned.

**What geographic region is Astronomer's Kubernetes Cluster?**

Astronomer's GKE cluster is in us-east-4.

**What can I use to test this out locally?**

[Microk8s](https://microk8s.io/) is a great way to run devops-free Kubernetes for testing and offline development. You're free to use [Minikube](https://kubernetes.io/docs/setup/minikube/) as well. 

**Can I pull images from a Private Registry?**

Yes. To do so, you'll have to create a `dockerconfigjson` using your existing Docker credentials.

If you're using Astronomer Cloud, you'll have to securely send it over to us. We can create a Kubernetes Secret in that namespace (with the `dockerconfigjson` in it), and give you the name of it for you to refer to in [your KubernetesPodOperator constructor](https://github.com/apache/airflow/blob/master/airflow/contrib/operators/kubernetes_pod_operator.py#L43-L46).

Give [this Kubernetes doc](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#registry-secret-existing-credentials) an initial read, and reach out to us to configure that first step. You'll have to take care of the rest!

**Do I have to add any Environment Variables to enable the KubePodOperator?**

Nope, you're good. The Kube config should be built-in.