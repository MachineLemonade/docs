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

1. [Select a base domain](https://astronomer.io/docs/ee-installation-base-domain)
1. [Get your machine setup with needed dev tools](https://astronomer.io/docs/ee-installation-dev-env)
1. [Get a Postgres server running](https://astronomer.io/docs/ee-installation-postgres)
1. [Obtain SSL](https://astronomer.io/docs/ee-installation-ssl)
1. [Setup DNS](https://astronomer.io/docs/ee-installation-dns)
1. [Install Helm and Tiller](https://astronomer.io/docs/ee-installation-helm)
1. [Set a few Kubernetes secrets](https://astronomer.io/docs/ee-installation-k8s-secrets)
1. [Build your config.yaml](https://preview.astronomer.io/docs/ee-configyaml/)

## Install Astronomer

You're ready to go!

```shell
helm install -f config.yaml . --namespace astronomer
```

Click the link in the output notes to log in to the Astronomer app.

Feel free to check out our video walkthrough of the Install below:

<iframe width="560" height="315" src="https://www.youtube.com/embed/IoeesuFNG9Q" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
