---
title: "General Kubernetes"
description: "Installing Astronomer Enterprise to your Kubernetes cluster."
date: 2018-10-12T00:00:00.000Z
slug: "ee-installation-general-kubernetes"
---

This guide describes the process to install Astronomer on a Kubernetes Cluster

## Are you admin-y enough to do this alone?

You will need to be able to:

* Obtain a wildcard SSL certificate
* Edit your DNS records
* Install/run Kubernetes command line tools to your machine

## Pre-requisites

Before running the Astronomer install command you must:

### 1) Select a base domain
You need to choose a base domain for your Astronomer installation, something like astro.mydomain.com. Each Airflow cluster you install will be accessible at a URL like unique-name-airflow.astro.mydomain.com and the admin application will be installed to app.astro.mydomain.com, the Grafana dashboard will be installed to grafana.astro.mydomain.com etc.

You will need to edit the DNS for this domain. If you work for a big company it might be easier to just register a new domain like astro-mycompany.com that you'll have full control of, and Astronomer can be installed on that root domain (app.astro-mycompany.com etc).

Note: For the purpose of our tutorial, our application domain is astro.mycompany.com.



### 2) Get the right dev tools:
You'll need some tools to interact with your Kubernetes cluster. This tutorial will assume [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) and the [Helm CLI] (https://helm.sh/docs/using_helm/#installing-helm)

### 3) Postgres
Astronomer uses Postgres the backend database. You can use any Postgres solution that can talk to the Kubernetes cluster you are deploying to, but we highly recommend using some sort of a managed database.

If you just want to get up and running quickly, the Stable Postgres helm chart is a great fit.

```
helm install --name astro-db stable/postgresql --namespace astronomer
```

(This assumes you are deployning the platform to the namespace labelled `astronomer`
  )
#### 4) SSL

You'll need SSL for certs between the platform components

Installing on a Subdomain
The base domain requirement is an absolute must to install the Astronomer platform. In order to properly install each part of our platform, we'll need a base domain as a foundation.

We'd recommend doing the install either (1) on a subdomain or (2) acquiring a new domain, instead of installing it on your root domain. If you don't have a preference, a good default subdomain is astro.

For the purpose of this guide, we'll continue to use astro.mydomain.com as an example.

You'll need to obtain a wildcard SSL certificate for *.astro.mydomain.com not only to protect the web endpoints (so it's https://app.astro.mydomain.com) but is also used by Astronomer inside the platfo rm to use TLS encryption between pods.

Buy a wildcard certificate from wherever you normally buy SSL
Get a free 90-day wildcard certificate from Let's Encrypt
We recommend purchasing a TLS certificate signed by a Trusted CA. Alternatively, you can follow the guide below to manually generate a trusted wildcard certificate via Let's Encrypt (90 day expiration). This certificate generation process and renewal can be automated in a production environment with a little more setup.

Note: Self-signed certificates are not supported on the Astronomer Platform.

Run (Linux):
```
docker run -it --rm --name letsencrypt -v /etc/letsencrypt:/etc/letsencrypt -v /var/lib/letsencrypt:/var/lib/letsencrypt certbot/certbot:latest certonly -d "*.astro.mycompany.com" --manual --preferred-challenges dns --server https://acme-v02.api.letsencrypt.org/directory
```
Run (macOS):
```
docker run -it --rm --name letsencrypt -v /Users/<my-username>/<my-project>/letsencrypt1:/etc/letsencrypt -v /Users/<my-username>/<my-project>/letsencrypt2:/var/lib/letsencrypt certbot/certbot:latest certonly -d "*/*.astro.mycompany.com"** --manual --preferred-challenges dns --server https://acme-v02.api.letsencrypt.org/directory
```
Note: This changes the 2 volume mount paths (beginning with -v before the colon) to host paths accessible to Docker for Mac.

Sample output:

Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator manual, Installer None
Obtaining a new certificate
Performing the following challenges:
dns-01 challenge for astro.mycompany.com

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
NOTE: The IP of this machine will be publicly logged as having requested this
certificate. If you're running certbot in manual mode on a machine that is not
your server, please ensure you're okay with that.

Are you OK with your IP being logged?
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(Y)es/(N)o: y

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Please deploy a DNS TXT record under the name
_acme-challenge.astro.mycompany.com with the following value:

0CDuwkP_vNOfIgI7RMiY0DBZO5lLHugSo7UsSVpL6ok

Before continuing, verify the record is deployed.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Press Enter to Continue
Follow the directions in the output to perform the domain challenge by adding the DNS TXT record mentioned. Follow your DNS provider's guidance for how to set the TXT record.

We recommend temporarily setting a short time to live (TTL) value for the DNS record should you need to retry creating the cert.

Renewing your Cert
To renew your cert, you have two options:

(1) Set to auto renew via a cert manager through kube-lego. More info about that here: http://docs.cert-manager.io/en/latest/index.html
(2) Generate a new short lived certificate and follow the same process to recreate your astronomer-tls secret after deleting the current one.
Note: After updating your secret, you'll also want to restart the houston, nginx and registry pods to ensure they pick up the new certificate.



### 5) [Setup DNS](https://astronomer.io/docs/ee-installation-dns)

Wherever you manage DNS for the base domain you chose, set an A record DNS setting *.<base domain> pointing to the static IP.

### 6) Install Helm and Tiller


To install the Astronomer Platform, you will need to also have helm and it's deployment service tiller installed. If you are already using helm, you can skip this step. To install Helm and Tiller, see the Kubernetes Helm Install Guide

Intialize Helm
Preparing for Helm with RBAC
If your cluster has RBAC enabled (usually by default in modern clusters), you'll need to take a few extra steps to give tiller the ability to talk to the Kubernetes API.

First, create a ServiceAccount and ClusterRole for tiller to use. Save the following to a file called rbac-config.yaml:

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
Then, run kubectl create -f rbac-config.yaml to create the resources in your cluster. After that, run helm init --service-account tiller to install tiller with the new service account. tiller should now have permissions to deploy charts.


1. [Set a few Kubernetes secrets](https://astronomer.io/docs/ee-installation-k8s-secrets)
1. [Build your config.yaml](https://preview.astronomer.io/docs/ee-configyaml/)



Wherever you manage DNS for the base domain you chose, set an A record DNS setting *.<base domain> pointing to the static IP.



## Install Astronomer

You're ready to go!

```shell
helm install -f config.yaml . --namespace astronomer
```

Click the link in the output notes to log in to the Astronomer app.

Feel free to check out our video walkthrough of the Install below:

<iframe width="560" height="315" src="https://www.youtube.com/embed/IoeesuFNG9Q" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


Wherever you manage DNS for the base domain you chose, set an A record DNS setting *.<base domain> pointing to the static IP.
