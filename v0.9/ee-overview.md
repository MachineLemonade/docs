---
title: "Enterprise Edition Overview"
date: 2018-10-12T00:00:00.000Z
slug: "ee-overview"
---

![Astronomer Overview](https://assets2.astronomer.io/main/docs/ee/astronomer_architecture_v0.8.png)

Astronomer Enterprise Edition allows you to run a private version of the Astronomer platform within your own Kubernetes.

## Astronomer Platform Deployment Components

### Astro CLI
Command Line tool for pushing deployments from your local machine to your workspaces running on Kubernetes. The CLI also provides the ability to launch a local stack via docker for local development and testing of DAGs, hooks and operators.

### Orbit React UI
A modern web based interface to create manage workspaces and deployments. Through the UI you can scale up or down your resources per deployment, invite new users and monitor Airflow logs

### Houston API
The core GraphQL API layer to interact with your astronomer workspaces and deployments. Use GraphQL queries directly, or integrate with your CI/CD platform to automate Airflow deployments.

### Docker Registry
Each Airflow deployment on your cluster will have it’s own set of required libraries and environment settings. Every time you create/update a deployment, a new docker image is built and pushed to a private registry created for your Astronomer platform. Kubernetes will pull from this registry when creating new pods.

### Commander
Commander is the provisioning component of the Astronomer Platform. It is responsible for interacting with the underlying infrastructure layer. gRPC service to communicate between our API and Kubernetes

### Prometheus
A monitoring platform used to collect metrics from StatsD. Prometheus collects Airflow metrics and pushes them to Granfana for visualization. Email alerts can also be setup to help quickly identify issues.

### Grafana
A web dashboard to help visualize and monitor Airflow metrics flowing in from Prometheus. Astronomer has pre-built plenty of dashboards to monitor your cluster or you can create your own custom dashboards to meet your needs.

### Alert Manager
Email alerts from Prometheus metrics. Enter emails for anyone you want to be alerted in the Orbit UI.These alerts can help notify you of issues on your cluster such as the Airflow Scheduler running slowly.

### NGINX
NGINX is used as an ingress controller to enforce authentication and direct traffic to the various services such as Airflow webserver, Grafana, Kibana etc. NGINX is also used to serve Airflow logs back up to the Airflow web UI from ElasticSearch.

### FluentD
FluentD is a data collector that is used to collect and push the Airflow log data into ElasticSearch.

### Elasticsearch
A powerful search engine used to centralize and index logs from Airflow deployments.

### Kibana
A web dashboard to help visualize all of your Airflow logs powered by ElasticSearch. Create your own dashboards to centralize your logs across all of your deployments.

### Prisma ORM
An interface between the HoustonGraphQL API and your Postgres database. This handles read/writes to your database as well as migrations for upgrades.

## Airflow Deployment Components

### Scheduler
Used to schedule Airflow DAGs and tasks. This process parses DAGs, determines dependencies and decides when DAGs should run and when tasks are ready to be scheduled. Tasks are sent to the celery task queue to be processed by Airflow workers

### Webserver
Airflow’s web UI used to view DAGs, Connections, variables, logs etc.

### Worker
A service running to process Airflow tasks. You can scale up the number of workers you have to increase the throughput of tasks in your environment. Uses celery distributed task queue

### Flower
Web UI for Celery distributed task queue. Used to monitor your Airflow worker services

###  pgBouncer
Provides connection pooling for Postgres. This helps prevent the Airflow database from being overwhelmed by too many connections.

### Redis
In memory data store used as the backend by the Celery task queue

### StatsD
Provides DAG and task level metrics from Airflow. Astronomer collects these metrics and pushes to a centralized view in Grafana

## Customer Supplied

### PostgreSQL Database
This is used as the backend for the Houston service as well as each Airflow deployment.

### Kubernetes environment
This consists of your Kubernetes control plane and fleet of worker nodes. (EKS, GKE, AKS) This is the core infrastructure that allows each of the above services to be run in a pod from a docker image. This coordinates communication between the services as well as fault tolerance if a pod crashes.
