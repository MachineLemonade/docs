---
title: "Managing Airflow Versioning on Astronomer"
description: "How to adjust Airflow version on Astronomer"
date: 2019-09-22T00:00:00.000Z
slug: "airflow-versioning"
---

## Overview

On Astronomer, the process of pushing up your code to an individual Airflow deployment involves customizing a locally built Docker image —— with your DAG code, Python Packages, plugins, and so on —— that's then bundled, tagged, and pushed to a Docker Registry (Astronomer's if you're using Astronomer Cloud, yours if you're running Astronomer Enterprise).

Included in that build is your `Dockerfile`, a file that is automatically generated when you initialize an Airflow project on Astronomer via our CLI. Every successful build on Astronomer must include a `Dockerfile` that references an Astronomer-created Docker Image built to be individually compatible with a particular Airflow version.

To upgrade or otherwise change the Airflow version you want to run, all it takes is a swap to the FROM statement held within your Dockerfile. For more information, read the guidelines below.

**Note:** Our current images are Alpine-Linux, but we intend to have full support for Debian-based images in coming releases.

## Changing your Airflow Version

### Overview

To change or upgrade the Airflow version on Astronomer Cloud, read the guidelines below.

**Note:** Astronomer Cloud is compatible with Airflow v1.9 - v1.10.4. Compatibility with Astronomer Enterprise will depend on the version of Astronomer that you're running.

### 1. Locate your Dockerfile in your Project Directory

When you initialiazed an Airflow project on Astronomer via our CLI, the following files should have been automatially generated:

```
.
├── dags # Where your DAGs go
│   ├── example-dag.py # An example dag that comes with the initialized project
├── Dockerfile # For Astronomer's Docker image and runtime overrides
├── include # For any other files you'd like to include
├── packages.txt # For OS-level packages
├── plugins # For any custom or community Airflow plugins
└── requirements.txt # For any Python packages
```

As a first step, open your directory's `Dockerfile` in a Code Editor.

### 2. Change the FROM Statement in your Dockerfile

Depending on the version of Airflow you want to run, you'll want to swap out the current FROM statement with the image you want to reference.

| Airflow Version | Docker Image                                        |
|-----------------|-----------------------------------------------------|
| v1.9             | FROM astronomerinc/ap-airflow:0.7.5-2-1.9.0-onbuild |
| v1.10.1          | FROM astronomerinc/ap-airflow:0.7.5-1.10.1-onbuild  |
| v1.10.2          | FROM astronomerinc/ap-airflow:0.8.2-1.10.2-onbuild  |
| v1.10.3          | FROM astronomerinc/ap-airflow:0.9.2-1.10.3-onbuild  |
| v1.10.4          | FROM astronomerinc/ap-airflow:0.10.0-1.10.4-onbuild |

### 3. Re-Build your Image

#### Local Development

If you're developing locally, make sure to save your changes and issue the following from your command line:

1. `$ astro airflow stop`

This will stop all 3 running Docker containers for each of the necessary Airflow components (Webserver, Scheduler, Postgres).

2. `$ astro airflow start`

This will start those 3 Docker containers needed to run Airflow. 

#### On Astronomer (Remote)

If you don't need to test this locally and just want to push to either Astronomer Cloud or your Astronomer Enterprise installation, you can issue:

```
$ astro airflow deploy
```

This will bundle your updated directory, re-build your image, and push it to your remote Airflow deployment.

### 5. Confirm your version in the Airflow UI

Once you've issued that command, navigate to your Airflow UI to confirm that you're now running the correct Airflow version.

#### Local Development

If you're developing locally, you can:

1. Head to http://localhost:8080/
2. Navigate to `About` > `Version`

Once there, you should see your correct Airflow version listed.

**Note:** The URL listed above assumes your Webserver is at Port 8080 (default). To change that default, read [this forum post](https://forum.astronomer.io/t/i-already-have-the-ports-that-the-cli-is-trying-to-use-8080-5432-occupied-can-i-change-the-ports-when-starting-a-project/48).

#### On Astronomer

If you're 




