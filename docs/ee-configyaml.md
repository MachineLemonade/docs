---
title: "Build your config.yaml"
description: "Installing config.yaml for Astronomer"
date: 2018-10-12T00:00:00.000Z
slug: "ee-configyaml"
---
Here, we'll set the configuration values for the Astronomer Helm chart.

`cd` to where you cloned `helm.astronomer.io`

Create a `config.yaml` for your domain setting overrides by copying [master.yaml](https://github.com/astronomer/helm.astronomer.io/blob/master/configs/master.yaml) if you don't already have one.

(If you are on GKE, you can use the GKE one).

```
cp master.yaml config.yaml
```

Change the branch on GitHub to match your desired Astronomer Platform version.

In `config.yaml`, set the following values:

```yaml
global:
  baseDomain: <your-basedomain>
  tlsSecret: astronomer-tls

astronomer:
  auth:
    google:
      enabled: true   
      clientId: <your-client-id>
      clientSecret: <your-client-secret>
```

Replace `<your-client-id>` and `<your-client-secret>` with the values from the previous step.

## Set up SMTP

You'll need to set up SMTP to use email invites with Astronomer.

In your Helm config, nested under `astronomer.smtp.uri` add something like:

```yaml
astronomer:
  smtp:
    uri: "smtp://user:pass@email-smtp.us-east-1.amazonaws.com/?requireTLS=true"
```
**Note**: We send emails using [nodemailer](https://nodemailer.com/smtp/).
