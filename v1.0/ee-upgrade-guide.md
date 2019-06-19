---
title: "Upgrade Astronomer"
description: "A guide to upgrading Astronomer on Enterprise"
date: 2018-07-17T00:00:00.000Z
slug: "ee-upgrade-guide"
---

1) Checkout the right version of Astronomer:

`$ git checkout v0.9.1`

2) Get the name of your platform release.

```
$ helm ls
NAME                       	REVISION	UPDATED                 	STATUS  	CHART                            	APP VERSION  	NAMESPACE
excited-armadillo          	1       	Mon Jun 17 18:05:48 2019	DEPLOYED	astronomer-0.8.2                 	0.8.2        	astronomer
```

Here, base platform release, `excited armadillo` lives in the `astronomer` namespace.

3) Upgrade helm/tiller to v2.14 or greater:

```
$ helm init --upgrade
```

Ensure you are on a version 2.14 or later:

```
$ helm version
Client: &version.Version{SemVer:"v2.14.1", GitCommit:"5270352a09c7e8b6e8c9593002a73535276507c0", GitTreeState:"clean"}
Server: &version.Version{SemVer:"v2.14.1", GitCommit:"5270352a09c7e8b6e8c9593002a73535276507c0", GitTreeState:"clean"}
```
_Note_: You may need to upgrade your local version of helm.

Brew (OS X):
```
$ brew upgrade kubernetes-helm
```

Ubuntu:
```
$ sudo snap refresh helm
```

4) Delete the Astronomer platform release.

```
$ helm delete --purge excited-armadillo
```

Wait until the pods in your platform namespace spin down, to watch them, run:

```
$ watch kubectl get pods -n astronomer
```

5) Install the new platform onto the old release and wait for all the pods to come up.

```
$ helm install -f config.yaml . -n excited-armadillo --namespace astronomer
```

You can watch the status of these with.

```
$ watch kubectl get pods --namespace astronomer
```
Once all pods are up in the `Running` state - the base platform has been upgraded!

6) Go to your app.BASEDOMAIN and log in (you may need to hard refresh (Cntrl+Refresh Button) the page for it to load).

7) Go into `Configure` for each Airflow deployment and Upgrade the Airflow instance and hit `Upgrade`.

8) Change the `FROM` line in your `Dockerfile` to

```
FROM astronomerinc/ap-airflow:0.9.1-1.10.3-onbuild
```

9) Upgrade your CLI:

```
$ astro upgrade
Astro CLI Version: v0.8.2  (2019.03.15)
Astro CLI Latest: v0.9.0  (2019.05.17)
There is a more recent version of the Astronomer CLI available.
You can install the latest tagged release with the following command
	$ curl -sL https://install.astronomer.io | sudo bash

```

10) Start pushing new DAGs!
