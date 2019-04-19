---
title: "Installing Astronomer CLI on Windows 10"
description: "Running the Astronomer CLI on the Windows subsystem for Linux."
date: 2018-08-24T00:00:00.000Z
slug: "cli-installation-windows-10"
---

Welcome to Astronomer!

If you're a Windows User looking to install and use the Astronomer CLI, you have 2 options:

1. Install the CLI directly on Windows 10
2. Install a Windows Subsystem for Linux (WSL)

## Astronomer CLI on Windows Subsystem for Linux (WSL)

This guide will walk you through the setup and configuration process for using the Astronomer CLI in the Windows Subsystem for Linux (WSL) on Windows 10. Before you start, make sure:
 - You're running the bash terminal
 - You have the [the WSL enabled](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
 - You're on Windows 10

**Note:** We use Ubuntu as our Linux flavor of choice, but this giude should work for other distrubutions as well.

Much of the setup process is borrowed from a guide written by Nick Janetakis. Find the full guide here: [Setting Up Docker for Windows and WSL to Work Flawlessly](https://docs.microsoft.com/en-us/windows/wsl/install-win10)

### Step 1. Install Docker CE for Windows

Follow the [Docker for Windows Install Guide](https://docs.docker.com/docker-for-windows/install/).

### Step 2. Expose the Docker Daemon

In your docker settings, under general, enable the `Expose daemon on tcp://localhost:2375 without TLS` setting.

This will allow the docker daemon running on windows to act as a remote docker service for our WSL instance.

### Step 3. Install Docker for Linux in WSL

In your WSL terminal, follow the Docker CE for Ubuntu install guide here: [Install Docker CE for Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

Docker wil lnot run in the WSL instance, however this will give us access to the docker cli through our linux environment.

### Step 4. Connect your WSL instance to Docker on Windows

Now, you need to point our docker host route to the remote docker daemon running in Windows. To do this we need to add an export path to our `~/.bashrc` file.

Run: `echo "export DOCKER_HOST=tcp://0.0.0.0:2375" >> ~/.bashrc && source ~/.bashrc` to add a new line to your bashrc file pointing the docker host to your exposed  daemon and re-source your bashrc file.

### Step 5. Custom mount points

To ensure docker can properly mount volumes, we need to create custom mount paths that work in the WSL instance.

**Note:** The process differs depending on the version of Windows 10 you're running. In our case we're running build 1709. See the full guide for more details about later builds).

First, create a new mount point directory:

`sudo mkdir /c`

Then bind this mount point:

`sudo  mount --bind /mnt/c /c`

You're all set! You can now run `docker run hello-world` through your WSL instance to ensure everything works as expected. Keep in mind that you will need to bind your mount point each time you start up a new WSL instance.

Once that's confirmed, head over to our [CLI Quickstart Guide](https://preview.astronomer.io/docs/cli-quickstart/) to finish the installation and start deployment DAGs.

## Astronomer CLI on Windows 10

If for any reason you can't install WSL, you can install the Astronomer CLI directly by following the instructions below.

### Step 1. Pre-Flight Checklist

Make sure you have the following installed:

- Windows 10
- [Docker](https://docs.docker.com/docker-for-windows/install/)

### Step 2. Enable Hyper-V

Make sure you enabled Hyper-V, which is required to run Docker and Linux Containers. 

If you have any issues with Docker, check out [Docker's Troubleshooting Guide for Windows](https://docs.docker.com/docker-for-windows/troubleshoot/).

### Step 3. Download the Astro CLI

Currently, Astronomer on Windows outside of WSL is only supported by Astronomer CLI versions v0.8.x.

To install our latest version, go [here](https://github.com/astronomer/astro-cli/releases/download/v0.8.2/astro_0.8.2_windows_386.zip).

### Step 4. Exract an Astro Windows file

After following step 3, you should see a zip file on your machine that contains the following:

- CHANGELOG
- README
- LICENSE
- A file titled `astro.exe`

Grab that `astro.exe` file and move it somewhere in your %PATH%. For more info on how to do so, check out [this doc]().

### Step 5. Final Command

Now, open your Terminal or PowerShell console and run the following:

```
C:\Windows\system32>astro version
Astro CLI Version: 0.8.2
Git Commit: f5cdab8f832da3c6184a7ac167b491e3bac3c022
```

You're all set! Happy Airflowing.

### Potential Postgres Error

As a Windows user, you might see the following error when trying to call `astro airflow start` on your newly created workspace:

```
Sending build context to Docker daemon  8.192kB
Step 1/1 : FROM astronomerinc/ap-airflow:latest-onbuild
# Executing 5 build triggers
 ---> Using cache
 ---> Using cache
 ---> Using cache
 ---> Using cache
 ---> Using cache
 ---> f28abf18b331
Successfully built f28abf18b331
Successfully tagged hello-astro/airflow:latest
INFO[0000] [0/3] [postgres]: Starting
Pulling postgres (postgres:10.1-alpine)...
panic: runtime error: index out of range
goroutine 52 [running]:
github.com/astronomer/astro-cli/vendor/github.com/Nvveen/Gotty.readTermInfo(0xc4202e0760, 0x1e, 0x0, 0x0, 0x0)
....
```

This is an issue pulling Postgres that should be fixed by running the following:

```
Docker pull postgres:10.1-alpine
```
