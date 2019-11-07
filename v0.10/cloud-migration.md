---
title: "Cloud Migration Kit"
description: "Everything you need to know to migrate to Astronomer's newest Cloud."
date: 2018-10-12T00:00:00.000Z
slug: "cloud-migration"
---

## Overview

After a long awaited release, our newly built Astronomer Cloud is finally ready for you. We've spent the past few months re-building our Cloud's infrastructure to optimize for scale, reliability, usability, and security.

Given the change in infrastructure, upgrading to Astronomer's latest (v0.10.3) involves a "migration" from one Astronomer-hosted Kubernetes cluster to another. To get set up, you have 2 paths:

**(1) Self-Migration**

In short, a self-migration requires that you:
 - Create an account on "New" Astronomer Cloud
 - Create and configure a new Deployment (Env Vars, resources, Airflow connections)
 - Start pushing up DAGs as soon as you're ready
 - Spin down your Deployments on "Old" Cloud

> **Note:** This option assumes that you do NOT want to migrate Airflow's metadata database for each of your deployments to the new Cloud cluster. This means you will not have a history of DAG/Task runs and will need to recreate any Airflow Variables, Connections, and Pools your DAGs might be using. With this process, you can slowly migrate DAGs one by one if you wish.

**(2) Astronomer Assisted Migration (Airflow DB Preserved)**

An Astronomer Assisted Migration requires that you:
- Turn your DAGs off
- Allow us to backup and restore your Airflow DB in a fresh deployment on "New" Astronomer Cloud
- Turn your DAGs back on

> **Note:** Depending on the size of your database, this process can be completed relatively quickly, though it requires that you migrate *all* DAGs within a deployment at once.

## Self-Migration

Below are the steps required for a self migration to our “New” Astronomer Cloud environment.

### Part I: Upgrade to Airflow v1.10.5

1. Upgrade all of your Airflow deployments on Astronomer Cloud to Airflow [v1.10.5](https://github.com/apache/airflow/blob/master/UPDATING.md)
     - To do so, you can update your Dockerfile to use the following image: `astronomerinc/ap-airflow:0.10.2-1.10.5-onbuild`

2. Ensure that your DAGs run smoothly on Airflow v1.10.5 either by testing locally with `astro dev start` or pushing them to your current Cloud deployments. 
     - The v1.10.5 image listed above is compatible with current Cloud 

### Part II: Set up on “New” Astronomer Cloud

Depending on the time of your migration, our team will either send you an invite to your new Workspace or expect that you create a new account and add users as needed.

1. Verify that you can login to the new Cloud cluster
    - URL: https://app.gcp0001.us-east4.astronomer.io/login
2. Re-create your Airflow Deployment(s) via the “New” Astronomer UI with appropriate resources
3. Manually generate your Airflow Connections, Variables and Pools in the Airflow UI
4. Re-create Environment Variables + Service Accounts in the Astronomer UI if needed
5. Whitelist “New” Astronomer Cloud’s IP address on any external systems your DAGs communicate with (e.g. AWS Redshift).
    - Static IP: `35.245.140.149`
6. Add your email address in the "Alerts" tab. These are platform-level alerts you can get more info on [here](https://www.astronomer.io/docs/alerts/)

> Note: If you leverage CI/CD, you'll have to replace our current Docker registry (`registry.astronomer.cloud`) with the registry on "New" Cloud (`registry.gcp0001.us-east4.astronomer.io`) in your script, in addition to your newly generated API Key.

### Part III: Upgrade the Astronomer CLI + Deploy

1. Upgrade your Astro CLI to our latest version. This is a MUST to authenticate.
    - `curl -sSL https://install.astronomer.io | sudo bash -s -- v0.10.2`
2. Authenticate to the new cluster via the CLI (once upgraded)
    - Auth Command:  `astro auth login gcp0001.us-east4.astronomer.io`
3. Pause DAGs on the old cluster
4. Deploy your project
    - `astro deploy`
5. Enable DAGs on the new cluster
    - Ensure your `start_date` and `catch_up` settings are appropriate so you don’t have duplicate DAG runs
6. If using CI/CD, update your CI/CD config file with your Service Account's new API key and deployment name

> **Note:** If you’re deploying code across the 2 Clouds, you WILL need to upgrade/downgrade your CLI version + authenticate to each accordingly.

## Astronomer Assisted Migration

If you'd like to preserve your deployment's Airflow database, we're more than happy to help. Follow the guidelines below.

### Part I: Upgrade to Airflow v1.10.5

1. Upgrade all of your Airflow deployments on Astronomer Cloud to Airflow v1.10.5
     - Update your Dockerfile to use the following image: 
     `astronomerinc/ap-airflow:0.10.2-1.10.5-onbuild`

2. Ensure that your DAGs run smoothly on Airflow v1.10.5 either by testing locally with `astro dev start` or pushing them to your current Cloud deployments. 
     - The v1.10.5 image listed above is compatible with the current Cloud

### Part II: Reach out to us

Once you've made sure that your DAGs can run successfully on Airflow v1.10.5, reach out to us via our [Support Portal](https://support.astronomer.io/hc/en-us/restricted).

When you reach out, please provide the following:

1. Confirmation that you're running Airflow v1.10.5 on *all* deployments you want to migrate
2. The "release name" of all Airflow deployments you want to migrate (e.g. `geodetic-planet-1234`)

From here, we'll take a look at your deployment's database and give you an estimate of how long the backup will take and schedule time with you to coordinate the migration.

> **Note:** Depending on the age of your deployment and the frequency at which your tasks run, this can take anywhere from 2 minutes to 1 hour.

## Frequently Asked Questions (FAQs)

**1. Will I experience any downtime?**

The process described above involves “pausing” your currently running DAGs and turning those same DAGs on in our new environment quickly thereafter.

If your DAGs run on short schedules, there may be some downtime during the migration. 

We encourage customers to:
- Perform this action at a time task execution is not at its peak
- Set `catchup=True` on any DAGs that you want DAG runs generated for during the downtime

**2. Do I HAVE to upgrade to Airflow v1.10.5?**

Yes. The only image compatible with Cloud 2 is Airflow v1.10.5, though we don't expect upgrading from prior Airflow versions to require significant changes.

Refer to [Airflow's v1.10.5](https://github.com/apache/airflow/blob/master/UPDATING.md) release notes for more detail on differences across versios.

**3. Will my Airflow DB be preserved?**

This is a choice you have. In the “Self Migration” process described above - no.

If you want to preserve your DB, please follow the guidelines above for an "Astronomer Assisted Migration" and reach out to us at [support@astronomer.io](mailto:support@astronomer.io).

**4. Can I wait to upgrade?**

If you’re not ready to upgrade, you may stay on current Cloud until December 31st, 2019.

**5. Will my Service Accounts and CI/CD process be affected?**

If you have a running CI/CD process that leverages an Astronomer Cloud API token, you will have to create a new service account with a newly generated API token on "New" Astronomer Cloud.

In your script, you'll have to replace our current Docker registry (`registry.astronomer.cloud`) to the new one, e.g.:

```
docker build . -t registry.gcp0001.us-east4.astronomer.io/{deployment-release-name}/airflow:$TAG
docker login registry.gcp0001.us-east4.astronomer.io -u _ -p ${NEW_API_SECRET_KEY}
docker push registry.gcp0001.us-east4.astronomer.io/{deployment-release-name}/airflow:$TAG```
```

**6. Will I have to re-add users?**

For those that Astronomer does not add for you, yes. Once you create a new Workspace on "New" Cloud, you will need to invite users again to your Workspace manually.

At this point, you will also be able to set their roles as either an Admin, Editor or Viewer.

**7. Do I have to re-enter payment information?**

You do not! We’ll take care of that for you.

If you want to *change* your current method of payment on file, you're free to enter a new credit card in the `Billing` tab of your Astronomer Workspace.

**8. Is this what all future releases will look like?**

This is a major platform upgrade. We anticipate future upgrades to be done in place and not require a migration.

**9. Will I be charged for usage on both "Old" Cloud and "New" Cloud if there’s an overlap?**

If you decide to pursue the "Self Migration" path, yes. You'll be charged per exact resource usage across both Clouds.

If you pursue the "Astronomer Assisted Migration" path, we'll make sure everything is running as expected in "New" Cloud and deprovision your Deployment(s) on "Old" Cloud soon thereafter accordingly.

**10. Can I use the Kubernetes Executor now?**

Yes. You’re free to transition to using the Kubernetes Executor in place of the Local or Celery Executors.









