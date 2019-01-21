---
title: "CI/CD"
description: "Using CI/CD with Astronomer."
date: 2018-10-12T00:00:00.000Z
slug: "ci-cd"
---

With Service accounts, you can deploy your DAGs with the continuous integration/continuous deployment (CI/CD) tool of your choice. This guide will walk you through configuring your CI/CD tool to use a Astronomer EE service accounts in order to build and push your Airflow project Docker images to the private Docker registry that is installed with Astronomer EE.

For background information and best practices on CI/CD, we recommend reading the article [An Introduction to CI/CD Best Practices](https://www.digitalocean.com/community/tutorials/an-introduction-to-ci-cd-best-practices) from DigitalOcean.

## Steps for Setting up CI/CD with Your Astronomer Airflow Project

Before we get started, this guide assumed you have installed Astronomer Enterprise Edition or are using Astronomer Cloud Edition, have the [astro-cli](https://github.com/astronomer/astro-cli) v0.6.0 or newer installed locally and are familiar with your CI/CD tool of choice. You can check your astro-cli version with the `astro version` command.

### Create a Service Account

In order to authenticate your CI/CD pipeline to the private Docker registry, you'll need to create a service account. This service account access can be revoked at any time by deleting the service account through the astro-cli or orbit-ui.

 Note that you're able to create Service Accounts at both the Workspace and Deployment level. Creating them at the Workspace level allows you to customize how your deployment pipeline works and allows you to deploy to multiple Airflow instances with one push, while creating them at the Deployment level ensures that your CI/CD pipeline will only deploy to that specific cluster.

 Here are a few examples of creating service accounts with various permission levels via the Astronomer CLI.

__Deployment Level Service Account__

```sa
astro service-account create -d [DEPLOYMENTUUID] --label [SERVICEACCOUNTLABEL]
```

__Workspace Level Service Account__

```sa
astro service-account create -w [WORKSPACEUUID] -l [SERVICEACCOUNTLABEL]
```

__System Level Service Account__

```sa
astro service-account create -s --label [SERVICEACCOUNTLABEL]
```

If you prefer to provision a service account through the orbit-ui you can create a service account on the project configuration page at the following link (replacing [BaseDomain] for your configured base domain).

In both cases, this will spit out an API key that will be used for the CI/CD process.

https://app.[BaseDomain]/login

### Configuring Your CI/CD Pipeline

Depending on your CI/CD tool, configuration will be slightly different. This section will focus on outlining what needs to be accomplished, not the specifics of how.
At it's core, your CI/CD pipeline will be authenticating to the private registry installed with the platform, then building, tagging and pushing an image to that registry.

An example pipeline (using DroneCI) could look like:

```yaml
pipeline:
  build:
    image: astronomerio/ap-build:0.0.7
    commands:
      - docker build -t registry.astronomer.cloud/infrared-photon-7780/airflow:ci-${DRONE_BUILD_NUMBER} .
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    when:
      event: push
      branch: [ master, release-* ]

  push:
    image: astronomerio/ap-build:0.0.7
    commands:
      - echo $${DOCKER_PASSWORD_TEST}
      - docker login registry.astronomer.cloud -u _ -p $${DOCKER_PASSWORD_TEST}
      - docker push registry.astronomer.cloud/infrared-photon-7780/airflow:ci-${DRONE_BUILD_NUMBER}
    secrets: [ docker_password_test ]
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    when:
      event: push
      branch: [ master, release-* ]
```

If you are using CircleCI, it might look like:
```
# Python CircleCI 2.0 configuration file
#
# Check https://circleci.com/docs/2.0/language-python/ for more details
#
version: 2
jobs:
  build:
    machine: true
    steps:
      - checkout
      - restore_cache:
          keys:
          - v1-dependencies-{{ checksum "requirements.txt" }}
          # fallback to using the latest cache if no exact match is found
          - v1-dependencies-

      - run:
          name: install dependencies
          command: |
            sudo apt-get update
            sudo apt-get -y install python3-pip
            pip install -r requirements.txt

      - run:
          name: run linter
          command: |
            pycodestyle .

      - save_cache:
          paths:
            - ./venv
          key: v1-dependencies-{{ checksum "requirements.txt" }}
  deploy:
    docker:
      - image:  astronomerio/ap-build:0.0.7
    steps:
      - checkout
      - setup_remote_docker:
          docker_layer_caching: true
      - run:
          name: Push to Docker Hub
          command: |
            TAG=0.1.$CIRCLE_BUILD_NUM
            docker build -t registry.datarouter.ai/empty-isotope-6604/airflow:ci-$TAG .
            docker login registry.datarouter.ai -u _ -p $DOCKER_KEY
            docker push registry.datarouter.ai/empty-isotope-6604/airflow:ci-$TAG

      - store_artifacts:
          path: test-reports
          destination: test-reports

workflows:
  version: 2
  build-deploy:
    jobs:
      - build
      - deploy:
          requires:
            - build
          filters:
            branches:
              only:
                - master
```


Breaking this down:

#### Authenticating to Docker

After you have created a service account, you will want to store the generated API key in an environment variable, or your secret management tool of choice.'

The first step of this pipeline is to authenticate against the registry:

```bash
docker login registry.$${BASE_DOMAIN} -u _ -p $${API_KEY_SECRET}
```

In this example, the BASE_DOMAIN is `astronomer.cloud` (for Astronomer Cloud). The `API_KEY_SECRET` is the API Key that you got from the CLI or the UI stored in your secret manager

#### Building and Pushing an Image

Once you are authenticated you can build, tag and push your Airflow image to the private registry, where a webhook will trigger an update of your Airflow deployment on the platform.

__Registry Address__
The registry address tells Docker where to push images to. In this case it will be the private registry installed with Astronomer EE, which will be located at registry.${BASE_DOMAIN}.

For example, if you are using Astronomer's cloud platform, you will use:
`registry.astronomer.cloud`

__Release Name__
Release name refers to the release name of your Airflow Deployment. It will follow the pattern of [SPACE THEMED ADJ.]-[SPACE THEMED NOUN]-[4-DIGITS] (in this example, `infrared-photon-7780`).

__Tag Name__
Tag name allows you to track all Airflow deployments made for that cluster over time. While the tag name can be whatever you want, we recommend denoting the source and the build number in the name.

In the below example we use the prefix `ci-` and the ENV `${DRONE_BUILD_NUMBER}`. This guarentees that we always know which CI/CD build triggered the build and push.

Example

```bash
docker build -t registry.${BASE_DOMAIN}/${RELEASE_NAME}/airflow:ci-${DRONE_BUILD_NUMBER} .
```

If you would like to see a more complete working example please visit our [full example using Drone-CI](https://github.com/astronomerio/example-dags/blob/master/.drone.yml).

Check out this video for a full walkthrough of this process:
<iframe width="560" height="315" src="https://www.youtube.com/embed/8h9lXzGa4sQ" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
