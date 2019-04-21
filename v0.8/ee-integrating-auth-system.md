---
title: "Integrating Auth Systems"
description: "Installing Astronomer on Azure's AKS."
date: 2018-10-12T00:00:00.000Z
slug: "ee-integrating-auth-system"
---
We're working on this guide right now - if you are trying to deploy here, drop us a line and we can help you through it.

By default, the Astronomer platform allows you to authenticate using your Google or GitHub account. We provide the option to authenticate using alternative providers through a platform called [Auth0](https://auth0.com/). Auth0 is an identity management platform that allows for seamless integration with numerous identity providers, including Azure Active Directory, LinkedIn, and Twitter. For a full list of supported identity providers, click [here](https://auth0.com/docs/identityproviders).

## 1. Create Auth0 Account
You'll need an Auth0 account in order to set up connections with the identity provider of your choice. Sign up for an Auth0 account [here](https://auth0.com/signup).

## Create Auth0 Tenant Domain
On initial login you'll be prompted to create a tenant domain. You can use the default or your own unique`tenant-name`. Your full tenant domain will look something like `astronomer.auth0.com`.

*NOTE - Your full tenant domain name may differ if you've created it outside the United States.*

## Create Connection between Auth0 and your Identity Management Provider

## Create Auth0 API

## Confiure Auth0 Application Settings

* app connections
  * enable / disable desired connections created in step ...
* edit default app settings
  * allowed callback URLs
  * allowed logout URLs
  * allowed origins

## 2. Configure Astronomer
```
astronomer:
  houston:
    config:
      auth:
        auth0:
          enabled: true
          clientId: ""
          baseDomain: ""
```