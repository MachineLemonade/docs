---
title: "Getting Started with Astronomer Certified Airflow"
description: "Everything you need to know to get up and running on Astronomer's distribution of Apache Airflow"
date: 2018-10-12T00:00:00.000Z
slug: "getting-started-cea"
---

## Overview

Designed in close partnership with both Airflow committers and users, Astronomer’s Certified Enterprise Airflow (CEA) offering is for teams ready to leverage the Python-based workflow management tool in production. CEA combines Airflow’s extensibility and community-driven development with industry standards for security, reliability, and scale.

## Get Started with CEA

### Install via Docker Image

The preferred way to install Astronomer CEA is to download our latest Astronomer-hosted Docker image, which will generally correspond with an open-source Airflow release.

To reference Astronomer's Docker Images, reference our public [Docker Hub repository](https://hub.docker.com/r/astronomerinc/ap-airflow).

Otherwise, read below for pre-requisites and install instructions.

#### Pre-Requisites

In order to install CEA on Docker, make sure you have the following pre-requisites on your machine:

- [Docker](https://www.docker.com/)
- [Python3](https://www.python.org/download/releases/3.0/)
- [virtualenv](https://pypi.org/project/virtualenv/)

To verify Docker is installed and your user has the right permissions, run:

```
docker run -it --rm hello-world
```

To verify Python3 is installed and in PATH, run:

```
python3 -c "print('Confirmed python3 installed.')"
```

To verify virtualenv is installed, run:

```
which virtualenv
```

#### Install

### Install via Python Wheel
