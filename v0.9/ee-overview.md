---
title: "Enterprise Edition Overview"
date: 2018-10-12T00:00:00.000Z
slug: "ee-overview"
---

![Astronomer Overview](https://assets2.astronomer.io/main/docs/ee/astronomer_architecture_v0.8.png)

Astronomer Enterprise Edition allows you to run a private version of the
Astronomer platform within your own Kubernetes.

It includes:

* Astronomer Command Center that includes an Astronomer-built UI, CLI, and a
  GraphQL API for easy cluster and deployment management on Kubernetes
* A Prometheus/Grafana/AlertManager monitoring stack
* ElasticSearch/FluentD/Kibana (EFK) log management stack
* Enterprise Authentication that supports Google Suite, SAML, Office 365, Active Directory, and more (via auth0)
* Enterprise-grade business day or business critical support

## Astro CLI

The [Astro CLI](https://github.com/astronomer/astro-cli)
helps you develop and deploy Airflow projects. Even if you are not interested in running Astronomer Enterprise, our CLI can be used to to run a containerized Airflow environment on your local machine.

## Houston API

[Houston](https://github.com/astronomer/houston-api) is a GraphQL
API that serves as the source of truth for the Astronomer Platform.

## Commander

[Commander](https://github.com/astronomer/commander) is a  GRPC
provisioning component of the Astronomer Platform. It is
responsible for interacting with the underlying Kubernetes
infrastructure layer.

## Orbit UI

[Orbit](https://github.com/astronomer/orbit-ui) is a GraphQL UI
that provides a clean interface to manage and scale Airflow environments.

## Monitoring

Astronomer Enterprise comes built in with a series of [Grafana charts](https://github.com/astronomer/astronomer/tree/master/docker/vendor/grafana/include) that give you real time metrics on each part of the Astronomer stack.

## dbBootstrapper

[dbBootstrapper](https://github.com/astronomer/db-bootstrapper)
is a utility that initializes databases and create Kubernetes
secrets, and runs automatically when an Airflow cluster is created.
