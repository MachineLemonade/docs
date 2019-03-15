---
title: "GCP GKE"
description: "Installing Astronomer on GCP GKE."
date: 2019-03-15T00:00:00.000Z
slug: "ee-installation-gke"
---

# GKE Installation
## Install necessary tools
* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [Google Cloud SDK](https://cloud.google.com/sdk/install)

* [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* [Helm](https://docs.helm.sh/using_helm/#installing-helm)
## Clone helm charts locally
    $ git clone https://github.com/astronomer/helm.astronomer.io.git
## Domain and SSL Setup
### Select base domain
### Obtain TLS certificate
## Configure GCP for Astronomer deployment
### Create GKE cluster
### Create static IP
### Create Kubernetes Namespace
## Configure Helm
### Create tiller service account and cluster role
### Deploy Tiller pod
## Deploy PostgreSQL Database
## Create Kubernetes Secrets
## Create Google OAuth Credentials
## Configure Helm Chart
## Install Astronomer
    $ helm install -f config.yaml . --namespace astronomer

<!-- This guide describes the process to install Astronomer on Google Cloud Platform (GCP).

## Are you admin-y enough to do this alone?

You will need to be able to:

* Obtain a wildcard SSL certificate
* Edit your DNS records
* Create resources on Google Cloud Platform
  (GKE admin permission)
* Install/run Kubernetes command line tools to your machine

## Pre-requisites

Before running the Astronomer install command you must:

1. [Select a base domain](https://astronomer.io/docs/ee-installation-base-domain)
2. [Get your machine setup with needed dev tools](https://astronomer.io/docs/ee-installation-dev-env)
3. [Setup GCP](https://astronomer.io/docs/ee-installation-gcp-setup)
4. [Get a Postgres server running](https://astronomer.io/docs/ee-installation-postgres)
5. [Obtain SSL](https://astronomer.io/docs/ee-installation-ssl)
6. [Setup DNS](https://astronomer.io/docs/ee-installation-dns)
7. [Install Helm and Tiller](https://astronomer.io/docs/ee-installation-helm)
8. [Set a few Kubernetes secrets](https://astronomer.io/docs/ee-installation-k8s-secrets)
9. [Create Google OAuth Creds ](https://astronomer.io/docs/ee-installation-google-oauth)
10. [Build your config.yaml](https://preview.astronomer.io/docs/ee-configyaml/)

## Install Astronomer

You're ready to go!

```shell
$ helm install -f config.yaml . --namespace astronomer
```

Click the link in the output notes to log in to the Astronomer app.

Feel free to check out our video walkthrough of the Install below:

<iframe width="560" height="315" src="https://www.youtube.com/embed/IoeesuFNG9Q" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> -->
