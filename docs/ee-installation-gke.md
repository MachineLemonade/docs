---
title: "GCP GKE"
description: "Installing Astronomer on GCP GKE."
date: 2019-03-15T00:00:00.000Z
slug: "ee-installation-gke"
---

# Installing Astronomer on GCP GKE
## Install necessary tools
* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [Google Cloud SDK](https://cloud.google.com/sdk/install)
* [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* [Helm](https://docs.helm.sh/using_helm/#installing-helm)

## Clone helm charts locally
    $ git clone https://github.com/astronomer/helm.astronomer.io.git
## Choose a Suitable Domain and 
All Astronomer services will be tied to a base domain of your choice. You will need to add / edit DNS records under this domain, so make sure you have the proper privileges.

Here are some examples of accessible services when we use the base domain `astro.mydomain.com`:
* Astronomer UI: `app.astro.mydomain.com`
* New Airflow Deployments: `unique-name-airflow.astro.mydomain.com`
* Grafana Dashboard: `grafana.astro.mydomain.com`
* Kibana Dashboard: `kibana.astro.mydomain.com`



<!-- screenshot -->

## Configure GCP for Astronomer deployment
### Create a GCP project
```
$ gcloud auth login
```

```
$ gcloud projects create [PROJECT_ID]
```

Confirm
```
$ gcloud projects list
PROJECT_ID             NAME                PROJECT_NUMBER
astronomer-project     astronomer-project  364686176109
```

```
$ gcloud config set project [PROJECT_ID]
```

```
$ gcloud config set compute/zone [COMPUTE_ZONE]
```

### Create GKE cluster
Enable the [Google Kubernetes Engine API](https://console.cloud.google.com/apis/library/container.googleapis.com?q=kubernetes%20engine)

<!-- screenshot -->

```
$ gcloud container clusters create [CLUSTER_NAME] --zone [COMPUTE_ZONE]
```

### Create static IP
```
$ gcloud compute addresses create astronomer-ip --region us-east4 --project astronomer-project-190903
```

```
$ gcloud compute addresses describe astronomer-ip --region us-east4 --project astronomer-project-190903 --format 'value(address)'
```

### Create Kubernetes Namespace
```
$ kubectl create namespace <my-namespace>
```
## SSL Configuration
### Obtain TLS certificate
```
$ docker run -it --rm --name letsencrypt -v /etc/letsencrypt:/etc/letsencrypt -v /var/lib/letsencrypt:/var/lib letsencrypt certbot/certbot:latest certonly -d "*.astro.mycompany.com" --manual --preferred-challenges dns --server https:/acme-v02.api.letsencrypt.org/directory
```

## Configure Helm
### Create tiller service account and cluster role
Save the following in a file named `rbac-config.yaml`:
```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: tiller
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: tiller
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
  - kind: ServiceAccount
    name: tiller
    namespace: kube-system
```

Run the following command to apply these configurations to your Kubernetes cluster:
```
$ kubectl create -f rbac-config.yaml
```

### Deploy Tiller pod
Your Helm client communicates with your kubernetes cluster through a `tiller` pod.  To deploy your tiller, run:
```
$ helm init --service-account tiller
```

## Deploy PostgreSQL Database
```
$ helm install --name <my-astro-db> stable/postgresql --namespace <my-namespace>
```

## Create Kubernetes Secrets
```
$ export PGPASSWORD=$(kubectl get secret --namespace <my-namespace> <my-astro-db>-postgresql -o jsonpath="{.data.postgresql-password}" | base64 --decode; echo)
```

Confirm your `$PGPASSWORD` variable is set properly:
```
$ echo $PGPASSWORD
```

```
$ kubectl create secret generic astronomer-bootstrap --from-literal connection="postgres://postgres:$PGPASSWORD@<my-astro-db>-postgresql.<my-namespace>.svc.cluster.local:5432" --namespace <my-namespace>
```

```
$ kubectl create secret tls astronomer-tls --key /etc/letsencrypt/live/astro.mycompany.com/privkey.pem --cert /etc/letsencrypt/live/astro.mycompany.com/fullchain.pem --namespace <my-namespace>
```

## Create Google OAuth Credentials
## Configure Helm Chart
## Install Astronomer
```
$ helm install -f config.yaml . --namespace astronomer
```
