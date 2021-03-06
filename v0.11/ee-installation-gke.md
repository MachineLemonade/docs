---
title: "GCP GKE Installation Guide"
description: "How to install Astronomer on Google Cloud Platform (GCP)."
date: 2019-03-15T00:00:00.000Z
slug: "ee-installation-gke"
---

This guide describes the steps to install Astronomer on Google Cloud Platform (GCP), which allows you to deploy and scale any number of [Apache Airflow](https://airflow.apache.org/) deployments within an [GCP Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine/) cluster.

## 1. Install Necessary Tools

* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [Google Cloud SDK](https://cloud.google.com/sdk/install)
* [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* [Helm v2.14.1](https://github.com/helm/helm/releases/tag/v2.14.1)
* SMTP Creds (Mailgun, Sendgrid) or any service will  work!
* Permissions to create / modify resources on Google Cloud Platform
* A wildcard SSL cert (we'll show you how to create a free 90 day cert in this guide)!


## 2. Choose a Suitable Domain

All Astronomer services will be tied to a base domain of your choice. You will need the ability to add / edit DNS records under this domain. Here are some examples of accessible services when we use the base domain `astro.mydomain.com`:

* Astronomer UI: `app.astro.mydomain.com`
* New Airflow Deployments: `unique-name-airflow.astro.mydomain.com`
* Grafana Dashboard: `grafana.astro.mydomain.com`
* Kibana Dashboard: `kibana.astro.mydomain.com`

## 3. Configure GCP for Astronomer Deployment

> Note: You can view Google Cloud Platform's Web Console at https://console.cloud.google.com/

### Create a GCP Project

Login to your Google account with the `gcloud` CLI:
```
$ gcloud auth login
```

Create a project:
```
$ gcloud projects create [PROJECT_ID]
```

Confirm the project was successfully created:
```
$ gcloud projects list
PROJECT_ID             NAME                PROJECT_NUMBER
astronomer-project     astronomer-project  364686176109
```

Configure the `gcloud` CLI for use with your new project:
```
$ gcloud config set project [PROJECT_ID]
```

Set your preferred compute zone, which will have a compute region tied to it.

You'll need this later on:

```
$ gcloud compute zones list
$ gcloud config set compute/zone [COMPUTE_ZONE]
```

### Create a GKE Cluster

Astronomer will deploy to Google's managed Kubernetes service (Google Kubernetes Engine). Learn more about GKE [here](https://cloud.google.com/kubernetes-engine/).

Enable the [Google Kubernetes Engine API](https://console.cloud.google.com/apis/library/container.googleapis.com?q=kubernetes%20engine).

We recommend using `n1-standard-8` nodes as a starting sport, with a minimum of 3 nodes (24 CPUs). Astronomer platform and components takes ~11 CPUs and ~40GB of memory as the default overhead.

Create your Kubernetes cluster:

> Note: You can choose the machine type to use, but we recommend using larger nodes vs smaller nodes.

```
$ gcloud container clusters create [CLUSTER_NAME] --zone [COMPUTE_ZONE] --machine-type n1-standard-8 --enable-autoscaling --max-nodes 10 --min-nodes 3
```

**Note:** If you work with multiple Kubernetes environments, `kubectx` is an incredibly useful tool for quickly switching between Kubernetes clusters. Learn more [here](https://github.com/ahmetb/kubectx).


### Create a Static IP Address

Generate a static IP address:
```
$ gcloud compute addresses create astronomer-ip --region [COMPUTE_REGION] --project [PROJECT_ID]
```

View your newly generated IP address and record the output for use later on:
```
$ gcloud compute addresses describe astronomer-ip --region [COMPUTE_REGION] --project [PROJECT_ID] --format 'value(address)'
```

## 4. Configure Helm with your GKE Cluster

Helm is a package manager for Kubernetes. It allows you to easily deploy complex Kubernetes applications. You'll use helm to install and manage the Astronomer platform. Learn more about helm [here](https://helm.sh/).

### Create a Kubernetes Namespace

Create a namespace to host the core Astronomer Platform. If you are running through a standard installation, each Airflow deployment you provision will be created in a seperate namespace that our platform will provision for you, this initial namespace will just contain the core Astronomer platform.

```
$ kubectl create namespace <my-namespace>
```

### Create a tiller Service Account

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

### Deploy a tiller pod

Your Helm client communicates with your kubernetes cluster through a `tiller` pod.  To deploy your tiller, run:

```
$ helm init --service-account tiller
```

Confirm your `tiller` pod was deployed successfully:

```
$ helm version
```

## 5. Deploy a PostgreSQL Database

To serve as the backend-db for Airflow and our API, you'll need a running Postgres instance that will be able to talk to your Kubernetes cluster. We recommend using a dedicated Postgres since Airflow will create a new database inside of that Postgres for each Airflow deployment.

We recommend you deploy a PostgreSQL database through a cloud provider database service like Google Cloud SQL.  This will require the full connection string for a user that has the ability to create, delete, and updated databases and users.

For demonstration purposes, we'll use the PostgreSQL helm chart:

```
$ helm install --name <my-astro-db> stable/postgresql --namespace <my-namespace>
```

> Note: We recommend using a Postgres instance with 3CPUs and 10GB of memory.

## 6. SSL Configuration

You'll need to obtain a wildcard SSL certificate for your domain (e.g. `*.astro.mydomain.com`). This allows for web endpoint protection and encrypted communication between pods. Your options are:

* Purchase a wildcard SSL certificate from your preferred vendor.
* Obtain a free 90-day wildcard certificate from [Let's Encrypt](https://letsencrypt.org/).

### Obtain a Free SSL Certificate from Let's Encrypt

Linux:

```
$ docker run -it --rm --name letsencrypt -v /etc/letsencrypt:/etc/letsencrypt -v /var/lib/letsencrypt:/var/lib/letsencrypt certbot/certbot:latest certonly -d "*.astro.mydomain.com" --manual --preferred-challenges dns --server https://acme-v02.api.letsencrypt.org/directory
```

macOS:

```
$ docker run -it --rm --name letsencrypt -v /Users/<my-username>/<my-project>/letsencrypt1:/etc/letsencrypt -v /Users/<my-username>/<my-project>/letsencrypt2:/var/lib/letsencrypt certbot/certbot:latest certonly -d "*.astro.mydomain.com" --manual --preferred-challenges dns --server https://acme-v02.api.letsencrypt.org/directory
```

Follow the on-screen prompts and create a TXT record through your DNS provider. Wait a few minutes before continuing in your terminal.

### Create a DNS A Record

Create an A record through your DNS provider for `*.astro.mydomain.com` using your previously created static IP address.

## 7. Create Kubernetes Secrets

You'll need to create two Kubernetes secrets - one for the databases to be created and one for TLS.

### Create Database Connection Secret

Set an environment variable `$PGPASSWORD` containing your PostgreSQL database password:

```
$ export PGPASSWORD=$(kubectl get secret --namespace <my-namespace> <my-astro-db>-postgresql -o jsonpath="{.data.postgresql-password}" | base64 --decode; echo)
```

Confirm your `$PGPASSWORD` variable is set properly:

```
$ echo $PGPASSWORD
```

Create a Kubernetes secret named `astronomer-bootstrap` to hold your database connection string:

```
$ kubectl create secret generic astronomer-bootstrap --from-literal connection="postgres://postgres:$PGPASSWORD@<my-astro-db>-postgresql.<my-namespace>.svc.cluster.local:5432" --namespace <my-namespace>
```

### Create TLS Secret

Create a TLS secret named `astronomer-tls` using the previously generated SSL certificate files:

```
$ sudo kubectl create secret tls astronomer-tls --key /etc/letsencrypt/live/astro.mydomain.com/privkey.pem --cert /etc/letsencrypt/live/astro.mydomain.com/fullchain.pem --namespace <my-namespace>
```

> Note: If you generated your certs using LetsEncrypt, you will need to run the command above as `sudo`

## 8. Configure your Helm Chart

Now that your Kubernetes cluster has been configured with all prerequisites, you can deploy Astronomer!

Clone the Astronomer helm charts locally and checkout your desired branch:

```
$ git clone https://github.com/astronomer/astronomer.git
$ git checkout <branch-name>
```

Create your `config.yaml` by copying our `starter.yaml` template:

```
$ cp ./configs/starter.yaml ./config.yaml
```

Set the following values in `config.yaml`:

* `baseDomain: astro.mydomain.com`
* `tlsSecret: astronomer-tls`
* `loadBalancerIP: <my-static-ip>`
* SMTP credentails as a houston config

Add the following line in the `nginx:` section:

* `preserveSourceIP: true`

Here is an example of what your `config.yaml` might look like:

```
#################################
### Astronomer global configuration
#################################
global:
  # Base domain for all subdomains exposed through ingress
  baseDomain: astro.mydomain.com

  # Name of secret containing TLS certificate
  tlsSecret: astronomer-tls

#################################
### Nginx configuration
#################################
nginx:
  # IP address the nginx ingress should bind to
  loadBalancerIP: 0.0.0.0
  preserveSourceIP: true

#################################
### SMTP configuration
#################################  

astronomer:
  houston:
    config:
      email:
        enabled: true
        smtpUrl: YOUR_URI_HERE
```

Note - the SMTP URI will take the form:

```
smtpUrl: smtps://USERNAME:PW@HOST/?pool=true
```

Check out our `Customizing Your Install` section for guidance on setting an [auth system](https://www.astronomer.io/docs/ee-integrating-auth-system/) and [resource requests(https://www.astronomer.io/docs/ee-configuring-resources/) in this `config.yaml`.

## 9. Install Astronomer

```
$ helm install -f config.yaml . --namespace <my-namespace>
```

## 10. Verify all pods are up

To verify all pods are up and running, run:

```
$ kubectl get pods --namespace <my-namespace>
```

You should see something like this:

```
$ kubectl get pods --namespace astronomer
NAME                                                    READY   STATUS      RESTARTS   AGE
newbie-norse-alertmanager-0                            1/1     Running     0          30m
newbie-norse-cli-install-565658b84d-bqkm9              1/1     Running     0          30m
newbie-norse-commander-7d9fd75476-q2vxh                1/1     Running     0          30m
newbie-norse-elasticsearch-client-7cccf77496-ks2s2     1/1     Running     0          30m
newbie-norse-elasticsearch-client-7cccf77496-w5m8p     1/1     Running     0          30m
newbie-norse-elasticsearch-curator-1553734800-hp74h    1/1     Running     0          30m
newbie-norse-elasticsearch-data-0                      1/1     Running     0          30m
newbie-norse-elasticsearch-data-1                      1/1     Running     0          30m
newbie-norse-elasticsearch-exporter-748c7c94d7-j9cvb   1/1     Running     0          30m
newbie-norse-elasticsearch-master-0                    1/1     Running     0          30m
newbie-norse-elasticsearch-master-1                    1/1     Running     0          30m
newbie-norse-elasticsearch-master-2                    1/1     Running     0          30m
newbie-norse-elasticsearch-nginx-5dcb5ffd59-c46gw      1/1     Running     0          30m
newbie-norse-fluentd-gprtb                             1/1     Running     0          30m
newbie-norse-fluentd-qzwwn                             1/1     Running     0          30m
newbie-norse-fluentd-rv696                             1/1     Running     0          30m
newbie-norse-fluentd-t8mqt                             1/1     Running     0          30m
newbie-norse-fluentd-wmjvh                             1/1     Running     0          30m
newbie-norse-grafana-57df948d9-jv2m9                   1/1     Running     0          30m
newbie-norse-houston-dbc647654-tcxbz                   1/1     Running     0          30m
newbie-norse-kibana-58bdf9bdb8-2j67t                   1/1     Running     0          30m
newbie-norse-kube-state-549f45544f-mcv7m               1/1     Running     0          30m
newbie-norse-nginx-7f6b5dfc9c-dm6tj                    1/1     Running     0          30m
newbie-norse-nginx-default-backend-5ccdb9554d-5cm5q    1/1     Running     0          30m
newbie-norse-orbit-d5585ccd8-h8zkr                     1/1     Running     0          30m
newbie-norse-prisma-699bd664bb-vbvlf                   1/1     Running     0          30m
newbie-norse-prometheus-0                              1/1     Running     0          30m
newbie-norse-registry-0                                1/1     Running     0          30m
```

If you are seeing issues here, check out our [guide on debugging your installation](https://astronomer.io/docs/ee-debugging-install/)

## 11. Access Astronomer's Orbit UI

Go to app.BASEDOMAIN to see the Astronomer UI.

## 12. Verify SSL  

To make sure that the certs were accepted, log into the platform and head to `app.BASEDOMAIN/token` and run:

`curl -v -X POST https://houston.BASEDOMAIN/v1 -H "Authorization: Bearer <token>"`

Verify that this output matches with:

`curl -v -k -X POST https://houston.BASEDOMAIN/v1 -H "Authorization: Bearer <token>"`
(The `-k` flag will run the command without looking for SSL)

Finally, to make sure the registry accepted SSL, try to log into the registry:

```
docker login registry.BASEDOMAIN -u _ p <token>
```
