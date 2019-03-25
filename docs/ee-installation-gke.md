---
title: "GCP GKE"
description: "Installing Astronomer on GCP GKE."
date: 2019-03-15T00:00:00.000Z
slug: "ee-installation-gke"
---

# Installing Astronomer on GCP GKE

## 1. Install Necessary Tools
* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [Google Cloud SDK](https://cloud.google.com/sdk/install)
* [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* [Helm](https://docs.helm.sh/using_helm/#installing-helm)

<!-- kubectx? -->

## 2. Choose a Suitable Domain
All Astronomer services will be tied to a base domain of your choice. You will need the ability to add / edit DNS records under this domain.

Here are some examples of accessible services when we use the base domain `astro.mydomain.com`:
* Astronomer UI: `app.astro.mydomain.com`
* New Airflow Deployments: `unique-name-airflow.astro.mydomain.com`
* Grafana Dashboard: `grafana.astro.mydomain.com`
* Kibana Dashboard: `kibana.astro.mydomain.com`
  
<!-- screenshot -->

## 3. Configure GCP for Astronomer Deployment
*NOTE - You can view Google Cloud Platform's Web Console at https://console.cloud.google.com/*

### Create a GCP Project

Authenticate the `gcloud` CLI with your Google account:
```
$ gcloud auth login
```

Create a project:
```
$ gcloud projects create [PROJECT_ID]
```

Confirm the project was successfully created:
```
$ gcloud projects list
PROJECT_ID             NAME                PROJECT_NUMBER
astronomer-project     astronomer-project  364686176109
```

Configure the `gcloud` CLI for use with your new project:
```
$ gcloud config set project [PROJECT_ID]
```

Set your preferred compute zone. *NOTE - The compute zone will have a compute region tied to it. You'll need this later on*:
```
$ gcloud compute zones list
$ gcloud config set compute/zone [COMPUTE_ZONE]
```

### Create a GKE Cluster
Enable the [Google Kubernetes Engine API](https://console.cloud.google.com/apis/library/container.googleapis.com?q=kubernetes%20engine)

<!-- screenshot -->

Create your Kubernetes cluster: 
```
$ gcloud container clusters create [CLUSTER_NAME] --zone [COMPUTE_ZONE] --machine-type n1-standard-4 --enable-autoscaling --max-nodes 10 --min-nodes 4
```

### Create a Static IP Address

Generate a static IP address:
```
$ gcloud compute addresses create astronomer-ip --region [COMPUTE_REGION] --project [PROJECT_ID]
```

View your newly generated IP address and record the output for use later on:
```
$ gcloud compute addresses describe astronomer-ip --region [COMPUTE_REGION] --project [PROJECT_ID] --format 'value(address)'
```

## 4. SSL Configuration

You'll need to obtain a wildcard SSL certificate for your domain (e.g. `*.astro.mydomain.com`). This allows for web endpoint protection and encrypted communication between pods. Your options are:
* Purchase a wildcard certificate from your preferred vendor.
* Obtain a free 90-day wildcard certificate from [Let's Encrypt](https://letsencrypt.org/).

### Obtain a Free SSL Certificate from Let's Encrypt
<!-- NEED TO COMPLETE -->
```
$ docker run -it --rm --name letsencrypt -v /etc/letsencrypt:/etc/letsencrypt -v /var/lib/letsencrypt:/var/lib letsencrypt certbot/certbot:latest certonly -d "*.astro.mycompany.com" --manual --preferred-challenges dns --server https:/acme-v02.api.letsencrypt.org/directory
```
Example output:
```
$ docker run -it --rm --name letsencrypt -v /etc/letsencrypt:/etc/letsencrypt -v /var/lib/letsencrypt:/var/lib/letsencrypt certbot/certbot:latest certonly -d "*.astro.datarouter.ai" --manual --preferred-challenges dns --server https://acme-v02.api.letsencrypt.org/directory
```
<!-- Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator manual, Installer None
Obtaining a new certificate
Performing the following challenges:
dns-01 challenge for astro.datarouter.ai

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
NOTE: The IP of this machine will be publicly logged as having requested this
certificate. If you're running certbot in manual mode on a machine that is not
your server, please ensure you're okay with that.

Are you OK with your IP being logged?
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(Y)es/(N)o: y

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Please deploy a DNS TXT record under the name
_acme-challenge.astro.datarouter.ai with the following value:

lqq19Uazhj7nXNz4nscCyCj997xr2ddD6sWnSgkX2qc

Before continuing, verify the record is deployed.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Press Enter to Continue
``` -->

Deploy a TXT record using the values in the output above:

<!-- screenshot -->

Wait a few minutes before continuing in your terminal:
<!-- ```
Waiting for verification...
Cleaning up challenges

IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/astro.datarouter.ai/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/astro.datarouter.ai/privkey.pem
   Your cert will expire on 2019-06-18. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot
   again. To non-interactively renew *all* of your certificates, run
   "certbot renew"
 - If you like Certbot, please consider supporting our work by:

   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le
``` -->

## 5. Configure Helm with your GKE Cluster
### Create a Kubernetes Namespace
```
$ kubectl create namespace <my-namespace>
```

### Create a `tiller` Service Account
Save the following in a file named `rbac-config.yaml`:
```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: tiller
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: tiller
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
  - kind: ServiceAccount
    name: tiller
    namespace: kube-system
```

Run the following command to apply these configurations to your Kubernetes cluster:
```
$ kubectl create -f rbac-config.yaml
```

### Deploy a `tiller` Pod
Your Helm client communicates with your kubernetes cluster through a `tiller` pod.  To deploy your tiller, run:
```
$ helm init --service-account tiller
```

Confirm your `tiller` pod was deployed successfully:
```
$ helm version
```
<!-- NOTE HELM CLIENT AND TILLER VERSION NEED TO MATCH -->

## 6. Deploy a PostgreSQL Database
```
$ helm install --name <my-astro-db> stable/postgresql --namespace <my-namespace>
```
<!-- BRING YOUR OWN POSTGRESQL -->

## 7. Create Kubernetes Secrets

### Create Database Connection Secret
Set an environment variable `$PGPASSWORD` containing your PostgreSQL database password:
```
$ export PGPASSWORD=$(kubectl get secret --namespace <my-namespace> <my-astro-db>-postgresql -o jsonpath="{.data.postgresql-password}" | base64 --decode; echo)
```

Confirm your `$PGPASSWORD` variable is set properly:
```
$ echo $PGPASSWORD
```

Create a Kubernetes secret named `astronomer-bootstrap` to hold your database connection string:
```
$ kubectl create secret generic astronomer-bootstrap --from-literal connection="postgres://postgres:$PGPASSWORD@<my-astro-db>-postgresql.<my-namespace>.svc.cluster.local:5432" --namespace <my-namespace>
```

### Create TLS Secret
Create a TLS secret named `astronomer-tls` using the previously generated certificate files:
```
$ sudo kubectl create secret tls astronomer-tls --key /etc/letsencrypt/live/astro.mycompany.com/privkey.pem --cert /etc/letsencrypt/live/astro.mycompany.com/fullchain.pem --namespace <my-namespace>
```

## 8. Create Google OAuth Credentials
<!-- NEED TO COMPLETE -->

## 9. Configure your Helm Chart
<!-- NEED TO COMPLETE -->

Clone the Astronomer helm charts locally and checkout your desired branch:
```
$ git clone https://github.com/astronomer/helm.astronomer.io.git
$ git checkout <branch-name>
```

```
$ cp /configs/starter.yaml ./config.yaml
```
<!-- WHY NOT JUST USE STARTER.YAML? -->
Set the following values:
* `baseDomain: `
* `tlsSecret: `
* `loadBalancerIP: `

## 10. Install Astronomer
```
$ helm install -f config.yaml . --namespace <my-namespace>
```
