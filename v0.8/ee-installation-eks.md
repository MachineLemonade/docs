---
title: "AWS EKS"
description: "Installing Astronomer on AWS EKS."
date: 2018-10-12T00:00:00.000Z
slug: "ee-installation-eks"
---
This guide describes the prerequisite steps to install Astronomer on Amazon Web Services (AWS).

# Installing Astronomer on AWS EKS

## 1. Install Necessary Tools

* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
* [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* [Helm](https://docs.helm.sh/using_helm/#installing-helm)
* SMTP Credentials (Mailgun, Sendgrid) or any service will  work!
* Permissions to create/modify resources on AWS
* A wildcard SSL cert (we'll show you how to create a free 90 day cert in this guide)

*NOTE - If you work with multiple Kubernetes environments, `kubectx` is an incredibly useful tool for quickly switching between Kubernetes clusters. Learn more [here](https://github.com/ahmetb/kubectx).*

## 2. Choose a Suitable Domain

All Astronomer services will be tied to a base domain of your choice. You will need the ability to add / edit DNS records under this domain.

Here are some examples of accessible services when we use the base domain `astro.mydomain.com`:

* Astronomer UI: `app.astro.mydomain.com`
* New Airflow Deployments: `unique-name-airflow.astro.mydomain.com`
* Grafana Dashboard: `grafana.astro.mydomain.com`
* Kibana Dashboard: `kibana.astro.mydomain.com`

## 3. Spin up the EKS Control Plane and a Kubernetes Cluster

You'll need to spin up the [EKS Control Plane](https://aws.amazon.com/eks/) as well as the worker nodes in your Kubernetes cluster. Amazon built EKS off of their pre-existing EC2 service, so you can manage your Kubernetes nodes the same way you would manage your EC2 nodes.

[This guide](https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html) by Amazon will take you through this process. **Before you go through this, keep in mind:**

* We generally advise running the EKS control plane in a single security group. The worker nodes you spin up should have the same setup as the EKS control plane.
* All security/access settings needed for your worker nodes should be configured in your Cloud Formation template.
* If you are creating the EKS cluster from the UI **only the user who created the cluster will have kubectl access to the cluster**. To give more users `kubectl` access, you'll have to configure that manually. [This post](http://marcinkaszynski.com/2018/07/12/eks-auth.html) goes through how IAM plays with EKS.
* Currently, the default EKS AMI does not work with Elasticsearch, which handles logs in the Astronomer platform. You'll have to use a different CloudFormation template found [here](https://forum.astronomer.io/t/elasticsearch-wont-work-on-eks/163/2)
* You'll be able to see each of your underlying nodes in the EC2 console. We recommend using 3 [t2.2xlarge](https://aws.amazon.com/ec2/instance-types/) nodes as a starting cluster size. You are free to use whatever node types you'd like, but Astronomer takes ~11 CPUs and ~40GB of memory as the default overhead. You can customize the default resource requests (see step 9).

## 4. Create a Stateful Storage Set

You'll need a stateful storage set for the persistent data Astronomer needs (mostly Airflow logs).

Create a new `.yaml` file (`storageclass.yaml`) that consists of:

```yaml
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: gp2
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
  fsType: ext4
```

Once you do that, you can run `kubectl apply -f storageclass.yaml`.

## 5. Create a Namespace and Configure Helm+Tiller

Create a namespace to host the core Astronomer Platform. If you are running through a standard installation, each Airflow deployment you provision will be created in a _seperate_ namespace that our platform will provision for you, this initial namespace will just contain the core Astronomer platform.

```bash
$ kubectl create ns astronomer
```

### Create a `tiller` Service Account
Save the following in a file named `rbac-config.yaml`:

```yaml
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

```bash
$ kubectl create -f rbac-config.yaml
```

### Deploy a `tiller` Pod
Your Helm client communicates with your kubernetes cluster through a `tiller` pod.  To deploy your tiller, run:

```bash
$ helm init --service-account tiller
```

Confirm your `tiller` pod was deployed successfully:

```bash
$ helm version
```

## 6. Configure Postgres

To serve as the backend-db for Airflow and our API, you'll need a running Postgres instance that will be able to talk to your Kubernetes cluster. We recommend using a dedicated Postgres since Airflow will create a new database inside of that Postgres for each Airflow deployment.

If you are using RDS, you'll need the full connection string for a user that has the ability to create, delete, and updated databases **and** users.

If you just want to get something up and running, you can also use the PostgreSQL helm chart:

```bash
$ helm install --name astro-db stable/postgresql --namespace astronomer
```

## 7. SSL Configuration

You'll need to obtain a wildcard SSL certificate for your domain (e.g. `*.astro.mydomain.com`). This allows for web endpoint protection and encrypted communication between pods. Your options are:

* Purchase a wildcard SSL certificate from your preferred vendor.
* Obtain a free 90-day wildcard certificate from [Let's Encrypt](https://letsencrypt.org/).

### Obtain a Free SSL Certificate from Let's Encrypt

If you are on a Mac:

```bash
$ docker run -it --rm --name letsencrypt -v /Users/<my-username>/<my-project>/letsencrypt1:/etc/letsencrypt -v /Users/<my-username>/<my-project>/letsencrypt2:/var/lib/letsencrypt certbot/certbot:latest certonly -d "*.astro.mydomain.com" --manual --preferred-challenges dns --server https://acme-v02.api.letsencrypt.org/directory
```

If you are running Linux:

```bash
$ docker run -it --rm --name letsencrypt -v /etc/letsencrypt:/etc/letsencrypt -v /var/lib/letsencrypt:/var/lib/letsencrypt certbot/certbot:latest certonly -d "*.astro.mydomain.com" --manual --preferred-challenges dns --server https://acme-v02.api.letsencrypt.org/directory
```

Follow the on-screen prompts and create a TXT record through your DNS provider. Wait a few minutes before continuing in your terminal.

## 7. Create Kubernetes Secrets

You'll need to create two Kubernetes secrets - one for the databases to be created and one for TLS.

### If you are using the PostgreSQL helm chart

Set an environment variable `$PGPASSWORD` containing your PostgreSQL database password:

```bash
$ export PGPASSWORD=$(kubectl get secret --namespace <my-namespace> <my-astro-db>-postgresql -o jsonpath="{.data.postgresql-password}" | base64 --decode; echo)
```

Confirm your `$PGPASSWORD` variable is set properly:

```bash
$ echo $PGPASSWORD
```

Create a Kubernetes secret named `astronomer-bootstrap` to hold your database connection string:

```bash
kubectl create secret generic astronomer-bootstrap \
  --from-literal connection="postgres://postgres:${PGPASSWORD}@astro-db-postgresql.astronomer.svc.cluster.local:5432" \
  --namespace astronomer
```

### If you are using RDS:

You'll need the full connection string for a user that has the ability to create, delete, and updated databases **and** users.

```bash
kubectl create secret generic astronomer-bootstrap --from-literal connection="postgres://postgres:$PGPASSWORD@<my-astro-db>-postgresql.<my-namespace>.svc.cluster.local:5432" --namespace <my-namespace>
```

**Note**: We recommend using a [t2 meduium](https://aws.amazon.com/rds/instance-types/) as the minimum RDS instance size.

### Create TLS Secret

Create a TLS secret named `astronomer-tls` using the previously generated SSL certificate files.

```bash
sudo kubectl create secret tls astronomer-tls --key /etc/letsencrypt/live/astro.mydomain.com/privkey.pem --cert /etc/letsencrypt/live/astro.mydomain.com/fullchain.pem --namespace <my-namespace>
```

**Note:** If you generated your certs using LetsEncrypt, you will need to run the command above as `sudo`

## 9. Configure your Helm Chart

Now that your Kubernetes cluster has been configured with all prerequisites, you can deploy Astronomer!

Clone the Astronomer helm charts locally and checkout your desired branch:

```
$ git clone https://github.com/astronomer/helm.astronomer.io.git
$ git checkout <branch-name>
```

Create your `config.yaml` by copying our `starter.yaml` template:

```
$ cp /configs/starter.yaml ./config.yaml
```


Set the following values in `config.yaml`:

* `baseDomain: astro.mydomain.com`
* `tlsSecret: astronomer-tls`
* SMTP credentails as a houston config

Here is an example of what your `config.yaml` might look like:

```yaml
#################################
## Astronomer global configuration
#################################
global:
  # Base domain for all subdomains exposed through ingress
  baseDomain: astro.mydomain.com

  # Name of secret containing TLS certificate
  tlsSecret: astronomer-tls


#################################
## Nginx configuration
#################################
nginx:
  # IP address the nginx ingress should bind to
  loadBalancerIP: ~

#################################
## SMTP configuration
#################################  

astronomer:
  houston:
    config:
      email:
        enabled: true
        smtpUrl: YOUR_URI_HERE

```

Note - the SMTP URI will take the form:

```
smtpUrl: smtps://USERNAME:PW@HOST/?pool=true
```

Check out our `Customizing Your Install` section for guidance on setting an (auth system)[https://www.astronomer.io/docs/ee-integrating-auth-system/] and (resource requests)[https://www.astronomer.io/docs/ee-configuring-resources/] in this `config.yaml`.

## 10. Install Astronomer

```
$ helm install -f config.yaml . --namespace <my-namespace>
```

## 11. Verify Pods are Up

To verify all pods are up and running, run:

```
kubectl get pods --namespace <my-namespace>
```

You should see something like this:

```command
virajparekh@orbiter:~/Code/Astronomer/docs$ kubectl get pods --namespace astronomer
NAME                                                    READY   STATUS      RESTARTS   AGE
newbie-norse-alertmanager-0                            1/1     Running     0          30m
newbie-norse-cli-install-565658b84d-bqkm9              1/1     Running     0          30m
newbie-norse-commander-7d9fd75476-q2vxh                1/1     Running     0          30m
newbie-norse-elasticsearch-client-7cccf77496-ks2s2     1/1     Running     0          30m
newbie-norse-elasticsearch-client-7cccf77496-w5m8p     1/1     Running     0          30m
newbie-norse-elasticsearch-curator-1553734800-hp74h    1/1     Running     0          30m
newbie-norse-elasticsearch-data-0                      1/1     Running     0          30m
newbie-norse-elasticsearch-data-1                      1/1     Running     0          30m
newbie-norse-elasticsearch-exporter-748c7c94d7-j9cvb   1/1     Running     0          30m
newbie-norse-elasticsearch-master-0                    1/1     Running     0          30m
newbie-norse-elasticsearch-master-1                    1/1     Running     0          30m
newbie-norse-elasticsearch-master-2                    1/1     Running     0          30m
newbie-norse-elasticsearch-nginx-5dcb5ffd59-c46gw      1/1     Running     0          30m
newbie-norse-fluentd-gprtb                             1/1     Running     0          30m
newbie-norse-fluentd-qzwwn                             1/1     Running     0          30m
newbie-norse-fluentd-rv696                             1/1     Running     0          30m
newbie-norse-fluentd-t8mqt                             1/1     Running     0          30m
newbie-norse-fluentd-wmjvh                             1/1     Running     0          30m
newbie-norse-grafana-57df948d9-jv2m9                   1/1     Running     0          30m
newbie-norse-houston-dbc647654-tcxbz                   1/1     Running     0          30m
newbie-norse-kibana-58bdf9bdb8-2j67t                   1/1     Running     0          30m
newbie-norse-kube-state-549f45544f-mcv7m               1/1     Running     0          30m
newbie-norse-nginx-7f6b5dfc9c-dm6tj                    1/1     Running     0          30m
newbie-norse-nginx-default-backend-5ccdb9554d-5cm5q    1/1     Running     0          30m
newbie-norse-orbit-d5585ccd8-h8zkr                     1/1     Running     0          30m
newbie-norse-prisma-699bd664bb-vbvlf                   1/1     Running     0          30m
newbie-norse-prometheus-0                              1/1     Running     0          30m
newbie-norse-registry-0                                1/1     Running     0          30m

```

## 12. Configure DNS

Now that you've successfully installed Astronomer, a new load balancer will have spun up for your Kubernetes cluster. You will need to create a new CNAME record in your DNS to route traffic to the ELB.

### If you are using route53 as your DNS provider:

Navigate to your newly created load balancer and copy the DNS name: route and use this to create a new wildcard CNAME record in you DNS. If your base domain is *organization.io* your wildcard record should be *.organization.io* and will route traffic to your ELB using that DNS name.

### 13. Verify You Can Access the Orbit UI

Go to `app.BASEDOMAIN` to see the Astronomer UI!
