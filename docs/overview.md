---
title: "Overview of Astronomer"
description: "An overview of our offerings."
date: 2018-10-12T00:00:00.000Z
slug: "overview"
---
# Product Overview 

## Astronomer: Cloud Edition

Astronomer Cloud is a managed offering of [Apache Airflow](https://airflow.apache.org/) on an Astronomer-hosted cluster for ultimate abstraction from all-things infrastructure. It includes:

- Secure and easy-to-spin-up Airflow environments with fully isolated resources

- An Astronomer-built [CLI](https://www.astronomer.io/docs/cli-getting-started/) for easy DAG deployment and management

- Access to Astronomer's [UI](https://app.astronomer.cloud/signup) with secure authentication for easy deployment, user, and workspace management

- Resource controls on Astronomer's UI

- Multiple [support options](https://www.astronomer.io/docs/support/) pending your team's needs

## Astronomer: Enterprise Edition

Astronomer Enterprise allows you to run a private version of our platform on your own Kubernetes cluster. It includes:

- Astronomer Command Center that includes an Astronomer-built UI, CLI, and a GraphQL API for easy cluster and deployment management on Kubernetes

- Access to a Prometheus and Grafana monitoring stack for metrics on your Airflow activity

- Enterprise Authentication that supports Google Suite, SAML, Office 365, Active Directory, and more through auth0.

- Enterprise-grade business day or business critical support

For our full installation guides, go to our [EE Getting Started Guide](https://www.astronomer.io/docs/ee-getting-started/).

# Platform Overview

## Airflow Deployment

When you create a new Airflow deployment on Astronomer, the
platform will deploy the following:

- Kubernetes pods for an Airflow Webserver
- Airflow Scheduler
- Pool of Celery workers
- A small Redis instance (that backs Celery)
- A statsd pod that streams metrics to a
centralized Prometheus and Grafana (*Enterprise only*)

Astronomer makes it easy to deploy these containers
to Kubernetes - but more importantly, to give Airflow developers a
CLI to deploy DAGs through a private Docker registry that interacts
with the Kubernetes API.

## Installation

Astronomer Cloud is a managed offering of Apache Airflow hosted on Astronomer. To get started, follow [this guide](https://www.astronomer.io/docs/getting-started/).

If you're interested in self-installing Astronomer onto Kubernetes our Enterprise Edition, follow our [install guides](https://www.astronomer.io/docs/ee-overview/).

When you install the Astronomer platform, a number of components
are deployed, including:

- NGINX
- Prometheus
- Grafana
- A GraphQL API (Houston)
- A React UI (Orbit)
- A Private Docker Registry (used
in the DAG deployment process).

Helm charts here: https://github.com/astronomer/helm.astronomer.io

## Authentication Options

- Local (username/password)
- Auth0 (supports SAML, Active Directory, other SSO)
- Google
- Github

## Astronomer Code

### Astronomer

The repository we consider the entrypoint to Astronomer is [astronomer/astronomer](https://github.com/astronomer/astronomer).

Here, we define all of our docker images and link out to the rest of our repositories. As our product and documentation grows and matures, this repo will do so as well.

### Helm Charts

This is what our Enterprise customers clone for an install: https://github.com/astronomer/helm.astronomer.io

We'd consider this repo our "umbrella" chart, since it contains several other charts that makeup our full system. 

 ### Astronomer CLI

The [Astro CLI](https://github.com/astronomer/astro-cli) is our very own Command Line tool designed to help you develop locally and push Airflow deployments with ease.

For a detailed breakdown, jump over to our [CLI Getting Started Guide](https://www.astronomer.io/docs/cli-getting-started/).

### Houston

[Houston](https://github.com/astronomer/houston-api) is a GraphQL
API that serves as the source of truth for the Astronomer Platform. Our GraphQL API is used to interact

We're currently doing a quick re-write [here](https://github.com/astronomer/houston-api-2).

### Commander

[Commander](https://github.com/astronomer/commander) is a GRPC
provisioning component of the Astronomer Platform. It is
responsible for interacting with the underlying Kubernetes
infrastructure layer.

### Orbit

[Orbit](https://github.com/astronomer/orbit-ui) is a GraphQL UI
that provides easy access to the capabilities of the Astronomer
platform.

### dbBootstrapper

[dbBootstrapper](https://github.com/astronomer/db-bootstrapper)
is a utility that initializes databases and create Kubernetes
secrets, and runs automatically when an Airflow cluster is created.
