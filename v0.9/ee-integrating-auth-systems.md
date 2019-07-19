---
title: "Integrating Auth Systems"
description: "Integrating Auth Systems with Auth0 and Okta"
date: 2019-04-21T00:00:00.000Z
slug: "ee-integrating-auth-systems"
---

By default, the Astronomer platform allows you to authenticate using your Google or GitHub account. We provide the option to authenticate using any alternative providers that follow the [Open Id Connect protocol](https://openid.net/connect/),  including (but not limited to) [Auth0](https://auth0.com/), [Okta](https://okta.com), and [Microsoft Azure's Active Directory](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-protocols-oidc). 

## Configuration

In your `config.yaml` file in your `helm.astronomer.io` directory, you can enable an OIDC provider of your choice via the following config:

```yaml
astronomer:
  houston:
    config:
      auth:
        openIdConnect:
        clockTolerance: 0 // A field that can optionally be set to adjust for clock skew on a user's machine.
          <provider-name>:
            enabled: true
            discoveryUrl: <provider-discovery-url>
            clientId: <provider-client-id>
            authUrlParams: // Additional required params set on case-by-case basis
```

## Okta Example

### Okta Configuration

1. Create an [Okta account](https://www.okta.com/) if you don't already have one you plan on using.

2. Create a new web app in your Okta account for Astronomer.

3. Set your `login redirect URI` to be `https://houston.BASEDOMAIN/v1/oauth/redirect`, where the `BASEDOMAIN` is the domain at which you're hosting your Astronomer installation.

4. Save the `Client ID` generated for this Okta app for use in the next steps.

### Astronomer Configuration

Add the following to your `config.yaml` file in your `helm.astronomer.io/` directory:

```yaml
astronomer:
  houston:
    config:
      auth:
        openIdConnect:
          okta:
            enabled: true
            clientId: "<okta-client-id>"
            baseDomain: "<okta-base-domain>"
```

Note that your okta-base-domain may be different from the basedomain of your Astronomer installation. You can read their docs on [finding your Okta domain](https://developer.okta.com/docs/api/getting_started/finding_your_domain/) if you are unsure what this value should be.


## Auth0 Example

### Auth0 Configuration

#### Create Auth0 Account

You'll need an Auth0 account in order to set up connections with the identity provider of your choice. Sign up for an Auth0 account [here](https://auth0.com/signup).

#### Create Auth0 Tenant Domain

On initial login you'll be prompted to create a tenant domain. You can use the default or your own unique`tenant-name`. Your full tenant domain will look something like `astronomer.auth0.com`.

*NOTE - Your full tenant domain name may differ if you've created it outside the United States.*

#### Create Connection between Auth0 and your Identity Management Provider

The steps required for establishing a connection will vary by identity provider. Auth0 provides connection guides for each identity provider [here](https://auth0.com/docs/identityproviders). Follow the link and click on your identity provider of choice for detailed instructions. Continue on to Step 4 once your connection is established.

#### Configure Auth0 Application Settings

**Enable / disable desired connections:**

* Navigate to `https://manage.auth0.com/dashboard/us/<tenant-name>/applications`.
* Under `Applications`, select `Default App`.
* Click the `Connections` tab. You should see your connection created in Step 3 listed here. Enable your new connection, and disable any connections that you won't be using.

**Edit the Default App settings:**

* Navigate to `https://manage.auth0.com/dashboard/us/<tenant-name>/applications`.
* Under `Applications`, select `Default App`.
* Click the `Settings` tab.
* Under `Allowed Callback URLs`, add `https://houston.<your-astronomer-base-domain>/v1/oauth/redirect`.
* Under `Allowed Logout URLs`, add `https://app.<your-astronomer-base-domain>/logout`.
* Under `Allowed Origins (CORS)`, add `https://*.<your-astronomer-base-domain>`.

**Create Auth0 API:**

* Navigate to `https://manage.auth0.com/dashboard/us/<tenant-name>/apis`.
* Click `+ Create API`.
* Under `Name`, enter `astronomer-ee`.
* Under `Identifier`, enter `astronomer-ee`.
* Leave the value under `Signing Algorithm` as `RS256`.

### Astronomer Configuration

Add the following to your `config.yaml` file in your `helm.astronomer.io/` directory. You can find your `clientID` value at `https://manage.auth0.com/dashboard/us/<tenant-name>/applications` listed next to `Default App`:

```yaml
astronomer:
  houston:
    config:
      auth:
        openIdConnect:
          auth0:
            enabled: true
            clientId: "<default-app-client-id>"
            baseDomain: "<tenant-name>.auth0.com"
```

#### Upgrade your Astronomer Deployment

If you're already running Astronomer, list your deployment release names and upgrade your deployment:
```
$ helm ls --namespace <your-namespace>
```
```
$ helm upgrade <release-name> -f config.yaml . --namespace <your-namespace>
```
