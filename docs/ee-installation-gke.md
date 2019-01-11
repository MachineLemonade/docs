---
title: "GCP GKE"
description: "Installing Astronomer on GCP GKE."
date: 2018-10-12T00:00:00.000Z
slug: "ee-installation-gke"
menu: ["Installation"]
position: [3]
---

This guide describes the process to install Astronomer on Google Cloud Platform (GCP).

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
10. [Build your config.yaml](https://astronomer.io/docs/ee-installation-config)

## Install Astronomer

You're ready to go!

```shell
$ helm install -f config.yaml . --namespace astronomer
```

Click the link in the output notes to log in to the Astronomer app.

Feel free to check out our video walkthrough of the Install below:

<iframe width="560" height="315" src="https://www.youtube.com/embed/IoeesuFNG9Q" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
