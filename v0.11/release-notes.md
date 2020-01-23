---
title: "Release Notes"
description: "Release notes for the Astronomer Platform"
date: 2020-01-20T00:00:00.000Z
slug: "release-notes"
---

## v0.11

### Platform-Wide Changes

**1. Support for a Debian-based Docker Image**

As of Astronomer v0.11, Astronomer Cloud officially supports a Debian-based Docker image in addition to all Alpine images we've made available.

Alpine is a widely-used lightweight distribution of Linux that keeps our images slim and performant, but nonetheless presents limitations for users looking to leverage Machine Learning Python libraries like `tensorflow` and `scikit-learn`. 

To use our v0.11 Debian image, throw this in your Dockerfile:
``

**2. Exposed Docker Image Tag in the Astronomer UI**

In an effort to expose more information to users on deploys, the tag of the latest Docker image pushed up to an Airflow Deployment is now listed in the Astronomer UI.

For example, users leveraging CI/CD can now verify what version of their code is running on our platform.

**3. Allow Astronomer Service Accounts access to the Airflow API**

Previously available on Astronomer v0.7.5, we've re-enabled the ability for users to leverage Astronomer Service Accounts to call the Airflow API.

Now, users can programmatically trigger DAGs via the Airflow API using a long-lasting Service Account instead of an authentication token that expires within 24Hours.

For guidelines, check out [this forum post](https://forum.astronomer.io/t/can-i-use-the-airflow-rest-api-to-externally-trigger-a-dag/162).

**4. Support for Airflow 1.10.6 and 1.10.7**

Astronomer v0.11 ships with a new set of Docker images for Airflow versions [1.10.6](https://github.com/apache/airflow/releases/tag/1.10.6rc1) and [1.10.7](https://github.com/apache/airflow/releases/tag/1.10.7)

**5. Bug Fixes & Stability Improvements**

### Astronomer Enterprise-Only

1. Support for a Debian-based Image
2. Exposed Docker Image Tag in the Astronomer UI
3. Allow Astronomer Service Accounts access to the Airflow API
4. Support for Airflow 1.10.6 and 1.10.7
5. Bug Fixes & Stability Improvements

#### Features

#### Bug Fixes