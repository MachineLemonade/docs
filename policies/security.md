---
title: "Security"
description: "Security sepcifications of the Astronomer platform."
date: 2018-10-12T00:00:00.000Z
slug: "security"
---

Astronomer allows you to dictate who has access to specific Airflow deployments.

We do this through a concept we call **Workspaces**.

Workspaces are conceptually similar to Teams, and are collections of Airflow
deployments that only specific users have access to, allowing you to ensure that
only those you want viewing your production deployments are capable of doing so.

In an upcoming release, we'll include Airflow 1.10 features, which will include
[role-based access control (RBAC)](https://medium.com/datareply/apache-airflow-1-10-0-released-highlights-6bbe7a37a8e1).

To learn more about Workspaces and see screenshots of what their user management
capability looks like, check out the [Platform Overview](https://astronomer.io/docs/overview).

## Cloud Edition

Astronomer Cloud is hosted on infrastructure we control. We run a single NAT
that all internet bound traffic flows through. We don't persist any of your
data, and all computation runs in short-lived containers that terminate after
the task is finished.

Our cluster and databases are all hosted in a private VPC with all private IPs. We connect to the cluster via SSH to a bastion node set up with authorized networks.

If you're interested in having a dedicated NAT or IP, you'll have to use our
Enterprise product, which is installed into your Kubernetes.

### Cloud Security FAQ

*What encryption algorithm do you use to encrypt data?*

We use AES to encrypt all data that is stored in underlying databases.

*Do you have a firewall in place?*

Yes, we use the GKE managed firewall rules at the VPC layer. [More on that here](https://cloud.google.com/kubernetes-engine/docs/concepts/security-overview#node_security).

*What PI data do you have access to?*

The only PI data we have access to is an email address associated with each account created on Astronomer Cloud?

*Do you encrypt client data at rest and during transfer?*

Secrets, credentials, and connection details pertaining to an Astronomer Workspace are stored as Environment Variables in the Astronomer UI and are encrypted both at rest and in transit as Kubernetes Secrets.

Our platform is additionally configured with a valid TLS certificate for our Cloud's base domain. All traffic to the system API and the docker registry is encrypted with this cert. Our system ensures that any sensitive data is encrypted in our database. We also ensure Airflow deployments are secured and configured with a Fernet Key to encrypt connection / variable data. All data related to payment is stored in Stripe and not in our database.

*Describe how client data is segregated and protected from other client’s data if in a multi-client environment.*

All customers are isolated within their own Postgres database with unique and randomly generated credentials that are randomly generated, secured and encrypted using Kubernetes Secrets. All customers are isolated inside of their own namespace within Kubernetes, with network policies, roles, and other security measures in place to ensure each tenant is truly isolated.

*Where is Astronomer Cloud hosted?*

Astronomer Cloud is hosted in GCP us-east1.

*How is logging handled in Astronomer Cloud?*

In Cloud, we allow user access to your scheduler, webserver, and worker logs via an EFK stack. As of now, you cannot pull the logs via API or download a pre-saved file - access to the raw files is only achievable via Astronomer Enterprise, which is an install of our platform in your own VPC.

Airflow-specific alerts for task and DAG run failures (or other triggers) can be configured via environment variables as needed.

## Enterprise Edition

Astronomer Enterprise is deployed in your cloud, on your Kubernetes. As such,
it should comply with your internal security specifications.
