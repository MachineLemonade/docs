---
title: "Integrating Auth Systems"
description: "Integrating Auth Systems with Auth0 and Okta"
date: 2019-04-21T00:00:00.000Z
slug: "ee-integrating-auth-systems"
---

By default, the Astronomer platform allows you to authenticate using your Google or GitHub account. We provide the option to authenticate using alternative providers via [Auth0](https://auth0.com/) and [Okta](https://okta.com). Auth0 is an identity management platform that allows for seamless integration with numerous identity providers, including Azure Active Directory, LinkedIn, and Twitter. For a full list of supported identity providers, click [here](https://auth0.com/docs/identityproviders).

## Okta Configuration

### In Okta

1. Create an [Okta account](https://www.okta.com/) if you don't already have one you plan on using.

2. Create a new web app in your Okta account for Astronomer.

3. Set your `login redirect URI` to be `https://houston.BASEDOMAIN/v1/oauth/redirect`, where the `BASEDOMAIN` is the domain at which you're hosting your Astronomer installation

4. Save the `Client ID` generated for this Okta app for use in the next steps.

### In Houston

1. In your Houston environment variables, make sure you have `"AUTH__OKTA__ENABLED="true"`. You can also disable Google, Github, and Auth0 if you don't plan on using any of these methods of authentication within your organization.

2. Create an environment variable called `AUTH_OKTA_CLIENT_ID` and set that equal to your Okta application's client ID.

3. Create a new environment variable called `AUTH_OKTA_BASE_DOMAIN` and set that equal to the basedomain of your Okta server. Note that this may be different from the basedomain of your Astronomer installation. You can read their docs on [finding your Okta domain](https://developer.okta.com/docs/api/getting_started/finding_your_domain/) if you are unsure what this value should be.

## Auth0 Configuration

### 1. Create Auth0 Account

You'll need an Auth0 account in order to set up connections with the identity provider of your choice. Sign up for an Auth0 account [here](https://auth0.com/signup).

### 2. Create Auth0 Tenant Domain

On initial login you'll be prompted to create a tenant domain. You can use the default or your own unique`tenant-name`. Your full tenant domain will look something like `astronomer.auth0.com`.

*NOTE - Your full tenant domain name may differ if you've created it outside the United States.*

### 3. Create Connection between Auth0 and your Identity Management Provider

The steps required for establishing a connection will vary by identity provider. Auth0 provides connection guides for each identity provider [here](https://auth0.com/docs/identityproviders). Follow the link and click on your identity provider of choice for detailed instructions. Continue on to Step 4 once your connection is established.

### 4. Configure Auth0 Application Settings

#### Enable / disable desired connections:

* Navigate to `https://manage.auth0.com/dashboard/us/<tenant-name>/applications`.
* Under `Applications`, select `Default App`.
* Click the `Connections` tab. You should see your connection created in Step 3 listed here. Enable your new connection, and disable any connections that you won't be using.

#### Edit the Default App settings:

* Navigate to `https://manage.auth0.com/dashboard/us/<tenant-name>/applications`.
* Under `Applications`, select `Default App`.
* Click the `Settings` tab.
* Under `Allowed Callback URLs`, add `https://houston.<your-astronomer-base-domain>/v1/oauth/redirect`.
* Under `Allowed Logout URLs`, add `https://app.<your-astronomer-base-domain>/logout`.
* Under `Allowed Origins (CORS)`, add `https://*.<your-astronomer-base-domain>`.

#### Create Auth0 API:

* Navigate to `https://manage.auth0.com/dashboard/us/<tenant-name>/apis`.
* Click `+ Create API`.
* Under `Name`, enter `astronomer-ee`.
* Under `Identifier`, enter `astronomer-ee`.
* Leave the value under `Signing Algorithm` as `RS256`.

### 5. Configure Astronomer

Add the following to your `config.yaml` file in your `helm.astronomer.io/` directory. You can find your `clientID` value at `https://manage.auth0.com/dashboard/us/<tenant-name>/applications` listed next to `Default App`:

```yaml
astronomer:
  houston:
    config:
      auth:
        auth0:
          enabled: true
          clientId: "<default-app-client-id>"
          baseDomain: "<tenant-name>.auth0.com"
```

### 6. Upgrade your Astronomer Deployment

If you're already running Astronomer, list your deployment release names and upgrade your deployment:
```
$ helm ls --namespace <your-namespace>
```
```
$ helm upgrade <release-name> -f config.yaml . --namespace <your-namespace>
```