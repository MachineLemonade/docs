---
title: "Release Notes"
description: "Astronomer Platform Release Motes"
date: 2020-01-24T00:00:00.000Z
slug: "release-notes"
---

## Astronomer v0.11 Release Notes

Release Date: January 24, 2020

### Platform-Wide Changes

#### Support for Airflow 1.10.6 and 1.10.7

Astronomer v0.11 ships with a new set of Docker images for Airflow versions [1.10.6](https://github.com/apache/airflow/releases/tag/1.10.6rc1) and [1.10.7](https://github.com/apache/airflow/releases/tag/1.10.7)in addition to our already-supported Airflow 1.10.5 image.

We've additionally de-coupled Astronomer and Airflow releases, which means each individual version of the Astronomer Platform is able to support a variety of Airflow images. For both Cloud and Enterprise users, this adds significant flexibiliy and lowers common incompatibility issues and dependencies across the board.

For a breakdown of supported Airflow Images on v0.11, refer to our [Airflow Versioning Doc](https://github.com/astronomer/docs/blob/v0.11/v0.11/airflow-versioning.md).

#### Support for a Debian-based Docker Image

Astronomer now officially supports a Debian-based Docker image in addition to all Alpine images we've made available.

Alpine is a widely-used lightweight distribution of Linux that keeps our images slim and performant, but nonetheless presents limitations for users looking to leverage Machine Learning Python libraries like `tensorflow` and `scikit-learn` that are often much easier to run on a Debian-based build.

To leverage a Debian Image on Astronomer v0.11, check out our [Airflow Versioning Doc](https://github.com/astronomer/docs/blob/v0.11/v0.11/airflow-versioning.md)

#### Exposed Docker Image Tag in the Astronomer UI

In an effort to expose more metadata on deploys to users, the tag of the latest Docker image pushed up to an Airflow Deployment is now listed in the "Deployment Configure" page of the Astronomer UI in addition to its existing place in CLI-generated output.
Moving forward, every push to Astronomer will generate a `deploy-n` tag, "n" representing the "number" of deploys made to that deployment. For example, `deploy-1` would represent a first code push, `deploy-2` the second, `deploy-3` the third, etc.
Users leveraging CI/CD can now verify what version of their code is running on our platform.

#### Allow Astronomer Service Accounts access to the Airflow API
Previously available on Astronomer v0.7.5, we've re-enabled the ability for users to leverage Astronomer Service Accounts to call the Airflow API.
Now, users can programmatically trigger DAGs via the Airflow API using a long-lasting Service Account instead of an authentication token that expires within 24Hours.
For guidelines, check out [this forum post](https://forum.astronomer.io/t/can-i-use-the-airflow-rest-api-to-externally-trigger-a-dag/162).

#### Bug Fixes & Stability Improvements

A few bug fixes and improvements:
- Improved Search in Astronomer's "Users Tab:
- "Back to Earth" link fixed in error page when Airflow is "Spinning Up"
- Added a raw URL to the "Confirm your Email" message upon sign-up
- Support for pre-pushing shared image layers to the platform for faster deploys

### Astronomer Enterprise

In addition to platform changes applicable to all Astronomer users, v0.11 shipped with additional features and improvements for those running Astronomer Enterprise.

#### Ability to Customize Platform-Wide User Permissions

We've created a new `USER` role that is synthetically bound to _all_ users within a single cluster and is entirely configurable, allowing Enterprise administrators to customize permissions for non-SysAdmin users across the platform.

For example, Enterprise administrators can now protect resource usage on the cluster by prohibiting non-SysAdmin users from creating Workspaces and provisioning Airflow deployments.

#### Support for Global Service Accounts

Astronomer now supports Global Service Accounts in addition to those that already exist at the Deployment and Workspace levels, empowering Enterprise SysAdmins to automate system-level API calls as needed.

## Prior Releases

To view release notes prior to Astronomer v0.11, refer to [our blog](/blog) or [changelog](https://github.com/astronomer/astronomer/blob/master/CHANGELOG.md) on Github.

Recent product release blog posts:

* [v0.10 Release](/blog/astronomer-v0-10-0-release)
* [v0.9 Release](/blog/astronomer-v0-9-0-release)
* [v0.8 Release](/blog/astronomer-v0-8-0-release)
* [v0.7 Release](/blog/astronomer-v0-7-0-release)
* [v0.6 Release](/blog/astronomer-v0-6-0-release)
* [v0.5 Release](/blog/astronomer-v0-5-0-release)