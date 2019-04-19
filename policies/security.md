---
title: "Security"
description: "Security specifications of the Astronomer platform."
date: 2018-10-12T00:00:00.000Z
slug: "security"
---

A deep respect for our customers and the data that they touch with their Airflow deployments has always been central to what we value here at Astronomer. We recognize that our customers use our products to run business-critical jobs that often involve sensitive data sets. That is why we have implemented a holistic security program that we continue to build upon with each of our product releases.

We use Google Cloud Platform internally for our Cloud datacenter and Kubernetes cluster, which means our customers benefit from GCP's comprehensive security practices and compliance certifications. We will also begin issuing regular penetration and vulnerability tests via a third party vendor for all versions of Astronomer 0.8 and later. It is our top priority to ensure your data is secure, so we look forward to building a company culture where security is deeply engrained.

## Cloud Edition

Astronomer Cloud is hosted on infrastructure that we control. To allow it to communicate with your systems, we run a single NAT that all internet bound traffic flows through. We don't persist any of your data, and all computation runs in short-lived containers that terminate after tasks are completed.

Our cluster and databases are all hosted in a private VPC with all private IPs. We connect to the cluster via SSH to a bastion node set up with authorized networks.

We also have a full Prometheus/Grafana monitoring stack that allows our employees to keep an eye on the health of all Airflow deployments running in Astronomer Cloud. We regularly check these dashboards and have alerts set up to notify our team if anything ever looks out of place.

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

*Do your users use MFA and/or IDP to login and authenticate to the service or management or infrastructure resources?*

To create an Astronomer Workspace, users have the option to authenticate via Google, GitHub, or username/password.

*Do you share any PI data with external entity or service?*

No, we never share any PI data with any external services.



## Enterprise Edition

Astronomer Enterprise is deployed in your cloud, on your Kubernetes. As such,
it will comply with your internal security specifications.
