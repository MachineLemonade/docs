---
title: "CLI Quickstart"
description: "Quickstart with the Astro CLI"
date: 2018-07-17T00:00:00.000Z
slug: "cli-quickstart"
---

## Prerequisites

First you must install [Docker](www.docker.com) on your computer. Then, install the Astro CLI.

If you are a Cloud customer, run:

```
curl -sSL https://install.astronomer.io | sudo bash -s -- 0.7.5
```

If you are an Enterprise customer, run:

```
curl -sSL https://install.astronomer.io | sudo bash

```

**Note:** The `curl` command will work for Unix (Linux+Mac) based systems. If you want to run on Windows 10, you'll need to run through [this guide](https://www.astronomer.io/docs/cli-installation-windows-10) on getting Docker for WSL working.

## Confirm the Install

Let's make sure you have Astro CLI installed on your machine, and that you have a project to work from.

```bash
astro
```

If you're set up properly, you should see the following:

```
astro is a command line interface for working with the Astronomer Platform.

Usage:
  astro [command]

Available Commands:
  airflow     Manage airflow projects and deployments
  auth        Mangage astronomer identity
  cluster     Manage Astronomer EE clusters
  config      Manage astro project configurations
  deployment  Manage airflow deployments
  help        Help about any command
  upgrade     Check for newer version of Astronomer CLI
  user        Manage astronomer user
  version     Astronomer CLI version
  workspace   Manage Astronomer workspaces

Flags:
  -h, --help   help for astro
```

For a breakdown of subcommands and corresponding descriptions, you can run: `astro help`

## Create a project

Your first step is to create a project to work from that lives in a folder on your local machine. The command you'll need is listed below, with an example `hello-astro` project.

 ```
mkdir hello-astro && cd hello-astro
astro airflow init
 ```

`astro airflow init` will build a base image from Astronomer's fork of Apache-Airflow using Alpine Linux. The build process will include everything in your project directory, which makes it easy to include any shell scripts, static files, or anything else you want to include in your code.

Once that command is run, you'll see the following skeleton project generated:

```bash
.
├── dags # Where your DAGs go
│   ├── example-dag.py
├── Dockerfile # For runtime overrides
├── include # For any other files you'd like to include
├── packages.txt # For OS-level packages
├── plugins # For any custom or community Airflow plugins
└── requirements.txt # For any python packages
```
The sample dag that gets generated has a few tasks that run bash commands

**Note:** The image will take some time to build the first time, after that it will build from cached layers.

Now you can run `astro airflow start` and see Airflow running on `localhost:8080/admin`

All changes made to the `dags` and `plugins` directory will be picked up automatically - any changes made to any of the other files will need the image to be rebuilt (`astro airflow stop` and `astro airflow start`).

For more information on using the CLI, see the Developing Locally with the CLI section.
