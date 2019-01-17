---
title: "Installing the CLI"
description: "How to get started using the Astro CLI on Mac, Linux, and Windows."
date: 2018-10-12T00:00:00.000Z
slug: "cli-installation"
menu: ["Astro CLI"]
position: [1]
---

The Astronomer CLI provides a local and dockerized version of Apache Airflow to use while writing your DAGs. Even if you're not using Astronomer, our CLI is an easy way to use Apache Airflow on your local machine.

## Prerequisites

To install the CLI, make sure you have the following on your machine:

- [Docker](https://www.docker.com/)
- [Go](https://golang.org/)

## Install

For the most recent version of our CLI, run the following command.

Via `curl`:

  ```bash
   curl -sSL https://install.astronomer.io | sudo bash
   ```

## Previous Versions

If you'd like to install a previous version of our CLI, the following command should do the trick:

Via `curl`:
   ```bash
    curl -sSL https://install.astronomer.io | sudo bash -s -- [TAGNAME]
   ```

To install CLI v0.7.5, for example, run:
   ```
curl -sSL https://install.astronomer.io | sudo bash -s -- v0.7.5
   ```

**Note:** If you get a mkdir error while going through the install, please download and run the [godownloader](https://raw.githubusercontent.com/astronomer/astro-cli/master/godownloader.sh) script locally.

    cat godownloader.sh | bash -s -- -b /usr/local/bin

## Windows 10

If you're interested in running the Astronomer CLI on the Windows 10 subsystem for Linux, [check out this doc](https://astronomer.io/docs/cli-installation-windows-10).
