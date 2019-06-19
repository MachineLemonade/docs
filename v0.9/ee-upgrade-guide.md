---
title: "Upgrade Astronomer"
description: "A guide to upgrading your installation of the Astronomer Enterprise platform"
date: 2019-06-19T00:00:00.000Z
slug: "ee-upgrade-guide"
---

To upgrade your installation of the Astronomer Enterprise platform, follow the guidelines below.

#### Pre-Requisites

- Access to an Astronomer Enterprise Installation (v0.8 or beyond)

### Checkout the latest Astronomer Version

As a first step, checkout the right version of Astronomer by running:

```
$ git checkout v0.9.1
```

### Get your Platform Release Name

To grab the name of your platform release, run:

```
$helm ls
```

You should see something like the following:

```
$ helm ls
NAME              REVISION UPDATED                   STATUS  	CHART             APP VERSION   NAMESPACE
excited-armadillo   1      Mon Jun 17 18:05:48 2019	 DEPLOYED	astronomer-0.8.2  0.8.2        	astronomer
```

In this output,

- Base Platform Release Name: `excited armadillo`
- Namespace: `astronomer`

### Upgrade Helm/Tiller

Now, upgrade Helm/Tiller to `v2.14` or greater.

```
$ helm init --upgrade
```

To ensure you're on v2.14 or later, run:

```
$ helm version
```

You should see something like the following:

```
$ helm version
Client: &version.Version{SemVer:"v2.14.1", GitCommit:"5270352a09c7e8b6e8c9593002a73535276507c0", GitTreeState:"clean"}
Server: &version.Version{SemVer:"v2.14.1", GitCommit:"5270352a09c7e8b6e8c9593002a73535276507c0", GitTreeState:"clean"}
```

#### Upgrade Local Version of Helm

You may need to upgrade your local version of Helm.

Brew (OS X):
```
$ brew upgrade kubernetes-helm
```

Ubuntu:
```
$ sudo snap refresh helm
```

### Delete your current Astronomer Platform Release

```
$ helm delete --purge <PLATFORM-RELEASE>
```

This will delete your current platform.

#### Wait for Pods to Spin Down

Wait until the Pods (FluentD, Grafana, etc.) in your platform namespace spin down. 

To watch them, run:

```
$ watch kubectl get pods -n <NAMESPACE>
```

### Install the New Platform

Now, let's re-install the platform onto the old release.

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

### Log In to the Astronomer UI

Now that the platform has been upgraded, go to `app.BASEDOMAIN` in your browser and log into Astronomer.

**Note:** You may need to hard refresh (Cntrl+Refresh Button) the page for it to load.

#### Upgrade Each Airflow Deployment

From here, we'll need to upgrade each of your Airflow Deployments in your Workspace(s). When you enter your Worksapce, you should see the list of deployments that are available for an Upgrade (they should all be, initially).

![Deployment List](https://assets2.astronomer.io/main/docs/upgrade-guide/upgrade-guide-deployment-list.png)

For each Deployment,

- Navigate to the `Configure` page
- Hit `Upgrade`

![Deployment Configure](https://assets2.astronomer.io/main/docs/upgrade-guide/upgrade-guide-deployment-configure.png)


**Note:** You can expect to hit a `404 Error` if you try to acces the Airflwo UI for any Airflow deployment that you have not upgraded.

### Update your Dockerfile

Let's make sure your image builds with the latest Astronomer version.

In your `Dockerfile`, change the `FROM` statement to:

```
FROM astronomerinc/ap-airflow:0.9.1-1.10.3-onbuild
```

### Upgrade your CLI

As a final step, you'll need to upgrade the Astronomer CLI to our latest version - `v0.9.1`.

To upgrade versions, run:

```
$ astro upgrade
```

Running that command should output your current version and confirm your upgrade versionm, as seen below:

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


