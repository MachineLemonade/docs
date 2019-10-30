---
title: "TERRAFORM AWS"
description: "Installing Astronomer on AWS with Terraform"
date: 2019-10-28T00:00:00.000Z
slug: "ee-installation-terraform-aws"
---

Terraform is a tool for building, changing, and versioning infrastructure safely and efficiently. Terraform can manage existing and popular service providers as well as custom in-house solutions.

You can read more about it here https://www.terraform.io/intro/index.html

## Install Astronomer with Terraform

Astronomer’s terraform scripts can be used to automate the provisioning of a production grade Airflow environment.

The Astronomer Enterprise module for AWS will provision the following resources in your AWS account:
* EKS cluster with an auto-scaling node group
* Aurora RDS
* VPC
* Subnets
* Full installation of Astronomer Enterprise 

You can find our module in the Terraform Registry here:
https://registry.terraform.io/modules/astronomer/astronomer-enterprise/aws/0.0.80

More detailed information can also be found here:
https://github.com/astronomer/terraform-aws-astronomer-enterprise

### Prerequisites

Install the necessary tools:

* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
* [AWS IAM Authenticator](https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html)
* [Terraform](https://www.terraform.io/downloads.html) *Use version 0.12.3 or later*
* [Helm client](https://github.com/helm/helm#install) *Use version 2.14.1 or later*
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) *Use version 1.12.3*


### Install necessary tools

#### Configure AWS CLI
Run the following command and enter the appropriate values when prompted. If you don't know the `AWS Access Key ID` or `AWS Secret Access Key` for your account, contact your AWS admin.

```
$ aws configure
AWS Access Key ID [None]: <key_id>
AWS Secret Access Key [None]: <access_key>
Default region name [None]: <region>
Default output format [None]: json
```

#### Create Config file

Create a config file to use to store the state of the terraform.

* `mkdir astro_terraform && cd astro_terraform`
* `vi main.tf`

```
terraform {
  backend "s3" {
	bucket = "bucket-name"
	key	= "astro_terraform"
	region = "us-east-1"
  }
}

module "astronomer-enterprise" {
  source                = "astronomer/astronomer-enterprise/aws"
  version               = "0.0.80"
  email                 = ""
  deployment_id         = "company_name"
  management_api        = "public"
  cluster_type          = "public"
  private_load_balancer = false
  route53_domain        = "airflow.com"
  min_cluster_size      = 6
  max_cluster_size      = 12
  db_instance_type      = db.r4.large
  worker_instance_type  = m5.xlarge

}
```

A full list of parameters can be found on the [Terraform Registry](https://registry.terraform.io/modules/astronomer/astronomer-aws/aws/1.1.29)


**Note:** The S3 backend is optional for state files. If not provided, state files will be stored locally.

#### Run Terraform
* `terraform init`
* `terraform apply`

This will generate an EKS cluster of the given worker_instance_size (that will scale between the minimum and maximum size).

This will use `<*.deployment_id>.<route53_domain>` as the base domain for the platform. Once the platform runs, navigate to `app.<deployment_id>.<route53_domain>` to verify the platform

A `kubeconfig` file will be generated in your working directory. Be sure to reference this file when running `kubectl` or `helm` commands. Example:
```
$ KUBECONFIG=./kubeconfig kubectl get pods -n astronomer
$ KUBECONFIG=./kubeconfig helm ls
```

#### Generate your config file

Once the terraform has successfully run, get the name of your release:

```
$ KUBECONFIG=./kubeconfig helm ls
NAME                       	REVISION	UPDATED                 	STATUS  	CHART                             	APP VERSION   	NAMESPACE                             
zealous-coral              	10      	Tue Oct  1 05:00:53 2019	DEPLOYED	astronomer-platform-0.10.1        	0.10.1        	astro     

$ KUBECONFIG=./kubeconfig helm get values zealous-coral >> config.yaml
```

This `config.yaml` file will contain the settings applied to your Astronomer deployment. Future changes to the helm charts can be run with:

```
$ KUBECONFIG=./kubeconfig helm upgrade <platform-name> -f config.yaml <path-to-charts> --namespace <namespace>
```

Note: `<path-to-charts>` should point to the version of the [Astronomer helm charts](https://github.com/astronomer/helm.astronomer.io), which were cloned locally when the terraform ran


### FAQs:

- Which subnets and VPCs will this deploy to?

Unless specified, a new VPC and subnets will be created. Specific subnets and VPC can be input into the `main.tf` file.]

- Can this be used to deploy to all private subnets?

- What if I don't use route53 as my DNS provider?
Right now, route53 is the only provider this module supports. We are working on dropping this requirement.

- What if I don't want to use a certificate from LetsEncrypt?
We are working on dropping this requirement.

