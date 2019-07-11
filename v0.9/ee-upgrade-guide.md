---
title: "Upgrade Astronomer"
description: "A guide to upgrading your installation of the Astronomer Enterprise platform"
date: 2019-06-19T00:00:00.000Z
slug: "ee-upgrade-guide"
---

To upgrade your installation of the Astronomer Enterprise platform, follow the guidelines below.

**Note:** This guide is **only** for upgrading from Astronomer v0.8.2 to v0.9.X.

For help upgrading between different versions, please contact us at support@astronomer.io.

#### Pre-Requisites

- Access to an Astronomer Enterprise Installation
- Access to the Kubernetes cluster hosting the Astronomer Platform.

### Checkout the latest Astronomer Version

Go into your `helm.astronomer.io` directory or wherever the config for your deployment lives.
Checkout the right version of the [Astronomer helm chart](https://github.com/astronomer/helm.astronomer.io)

```
$ git checkout v0.9.X
```

### Find the Platform Release Name

```
$helm ls

NAME              REVISION UPDATED                   STATUS  	CHART             APP VERSION   NAMESPACE
excited-armadillo   1      Mon Jun 17 18:05:48 2019	 DEPLOYED	astronomer-0.8.2  0.8.2        	astronomer
```


In this output,

- Base Platform Release Name: `excited-armadillo`
- Namespace: `astronomer`

Use the same `config.yaml` as before. If you do not have the `config.yaml`, you can regenerate it with `helm get values excited-armadillo >>config.yaml`.
This contains all the overrides and settings needed for your platform (basedomain, SMTP creds, etc.)

### Upgrade Helm/Tiller

Astronomer v0.9.X requires helm 2.14 or later.

```
$ helm version

Client: &version.Version{SemVer:"v2.14.1", GitCommit:"5270352a09c7e8b6e8c9593002a73535276507c0", GitTreeState:"clean"}
Server: &version.Version{SemVer:"v2.14.1", GitCommit:"5270352a09c7e8b6e8c9593002a73535276507c0", GitTreeState:"clean"}
```

To upgrade helm locally:

Brew (OS X):
```
$ brew upgrade kubernetes-helm
```

Ubuntu:
```
$ sudo snap refresh helm
```

Once the right version of Helm is running locally, it can be upgraded on the cluster:

```
$ helm init --upgrade
```

Run `helm version` again to verify the Helm and Tiller versions.  


### Delete your current Platform Release

```
$ helm delete --purge <PLATFORM-RELEASE>
```

This will delete your current platform release, but leave the secrets and metadata.

#### Wait for Pods to Spin Down

Wait until the Pods (FluentD, Grafana, etc.) in your platform namespace spin down. You can track this with:

```
$ watch kubectl get pods -n <NAMESPACE>
```

### Install the New Platform

Now, let's re-install the platform onto the old release to have it pick up the old platform's metadata,

**Note:** If you are running your platform in a fully private networking setup, add
```
nginx:
    privateLoadBalancer: True
```

into your `config.yaml`

```
$ helm install -f config.yaml . -n <PLATFORM-RELEASE> --namespace <NAMESPACE>
```

#### Wait for Pods to Spin Up

Once you do this, wait for all the Pods to come up.

You can watch them once again by running:

```
$ watch kubectl get pods --namespace <NAMESPACE>
```

Once all pods have reached `Running` state, you can consider the base platform upgraded.

### Log into the Astronomer UI

Now that the platform has been upgraded, go to `app.BASEDOMAIN` in your browser and log into Astronomer.

**Note:** You may need to hard refresh (Cntrl+Refresh Button) the page for it to load.

#### Upgrade Each Airflow Deployment

From here, we'll need to upgrade each of your Airflow Deployments in your Workspace(s). When you enter your Worksapce, you should see the list of deployments that are available for an Upgrade (they should all be, initially).

![Deployment List](https://assets2.astronomer.io/main/docs/upgrade-guide/upgrade-guide-deployment-list.png)

For each Deployment,

- Navigate to the `Configure` page
- Hit `Upgrade`

![Deployment Configure](https://assets2.astronomer.io/main/docs/upgrade-guide/upgrade-guide-deployment-configure.png)


**Note:** You can expect to hit a `404 Error` if you try to acces the Airflow UI for any Airflow deployment that you have not upgraded.

### Update your Dockerfile

The image in the Dockerfile should match with the new version of Astronomer
In your `Dockerfile`, change the `FROM` statement to:

```
FROM astronomerinc/ap-airflow:0.9.2-1.10.3-onbuild
```

Run `astro airflow start` with the new image to verify the new image builds. For a list of changes, see the [CHANGELOG](https://github.com/apache/airflow/blob/master/CHANGELOG.txt) on the Airflow Github. If you are seeing errors in previously working plugins, be sure to check if their import path changed with the new Airflow version.

### Upgrade your CLI

As a final step, upgrade the Astronomer CLI to a matching version

To upgrade versions, run:

```
$ astro upgrade
```

Running that command should output your current version and confirm your upgrade version, as seen below:

```
$ astro upgrade
Astro CLI Version: v0.8.2  (2019.03.15)
Astro CLI Latest: v0.9.1  (2019.05.17)
There is a more recent version of the Astronomer CLI available.
You can install the latest tagged release with the following command
	$ curl -sL https://install.astronomer.io | sudo bash

```

### Start Deploying DAGs

With that, you're all set to run on Astronomer's latest. You're free to push DAGs to your upgraded Deployments.

**Questions?**

If you have any issues or questions, don't hesitate to reach out to your dedicated support member or to our wider team at support@astronomer.io.
