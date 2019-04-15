---
title: "Setting up Airflow Email Alerts"
description: "How to set up Sendgrid to send Airflow email alerts"
date: 2019-01-14T00:00:00.000Z
slug: "setting-up-airflow-emails"
---

Airflow emails are a useful way to get notified of DAG retries, failures, and anything else you want to custom set through the [email util](https://github.com/apache/airflow/blob/master/airflow/utils/email.py). By default, Astronomer does not bundle in a SMTP service to send emails through Airflow but there are a number of easy (and free) options to include your own account.

This guide will walk through the setup of a free Sendgrid account and how to connect it to your Airflow deployment.

## Creating a Sendgrid token
Start by going to `https://signup.sendgrid.com` and sign up for a new account. You will need fill out some boilerplate survey information but will quickly be through to your account.

![Sendgrid Signup](https://assets2.astronomer.io/main/docs/emails/sendgrid_signup.png)

A new account will be given 40k emails for the first 30 days and then 100 emails/day for free. As long as your DAGs are working properly, this should be more than enough for most use cases.

After you create your account, you'll reach a view like below. Click on "Integrate using our Web API or SMTP relay".   
![Sendgrid Getting Started](https://assets2.astronomer.io/main/docs/emails/sendgrid_getting_started.png)

Choose the "Web API (recommended)" method.
![Sendgrid Setup Method](https://assets2.astronomer.io/main/docs/emails/sendgrid_setup_method.png)

Select the "cURL" option from the languages.
![Sendgrid Language](https://assets2.astronomer.io/main/docs/emails/sendgrid_language.png)

Create a new API Key (the name can be anything you want) and run the code in your terminal, and verify the integration. You don't have to export the API Key as the docs suggest as you can instead replace the $SENDGRID_API_KEY in the example code with the API key that has been generated.

If you don't execute the code to use the token at least once, Sendgrid will not be able to verify that it is working properly and you will not be able to use the key.
![Sendgrid API Key](https://assets2.astronomer.io/main/docs/emails/sendgrid_apikey.png)

Click "Verify" on the following page to make sure Sendgrid activates the key. If an error pops up that Sendgrid cannot find the test email, run the cURL command again in your terminal and click "Retry".

## Adding your Sendgrid credentials to your Astronomer deployment
Once you have your Sendgrid API Key, go to your Astronomer deployment and click "Configure" from the top nav. Click on "Environment Vars" from the lefthand menu and begin adding the following variables specified below. Your Sendgrid API Key will be used as the value for `SMTP__SMTP_PASSWORD`. You will also need to specify a `SMTP__SMTP_MAIL_FROM` value with the same email you used to sign up with Sendgrid.

```
SMTP__SMTP_HOST=smtp.sendgrid.net
SMTP__SMTP_STARTTLS=True
SMTP__SMTP_SSL=False
SMTP__SMTP_USER=apikey
SMTP__SMTP_PASSWORD={ENTER_SENDGRID_APIKEY_HERE}
SMTP__SMTP_PORT=587
SMTP__SMTP_MAIL_FROM={ENTER_RELEVENT_FROM_EMAIL_HERE}
```
![Astro Create Envs](https://assets2.astronomer.io/main/docs/emails/astro_create_envs.png)

Click `Update` to save the configuration and redeploy to propagate to your deployment. Your deployment will use that configuration to send emails from then on.

## Additional Configuration

For more insight on how each alert is triggered, it might be helpful to take a look at the [underlying configs](https://github.com/astronomer/helm.astronomer.io/blob/387bcfcc06885d9253c2e1cfd6a5a08428323c57/charts/prometheus/values.yaml#L99
). For example, you'll see that the alert `AirflowFailureRate` will occur at any given time relative to the failure rate for the prior two days, etc.

### Triggering Alerts on DAG Run

Email alerting set up via `email_on_failure` is handled at the task level. If a handful of your tasks fail for related reasons, you'll receive an individual email for each of those failures.

If you're interested in limiting failure alerts to the DAG run level, you can instead pass `on_failure_callback` ([source](https://github.com/apache/airflow/blob/v1-10-stable/airflow/models.py#L3311)) directly in your DAG file to define a Python function that sends you an email denoting failure.

```
 :param on_failure_callback: A function to be called when a DagRun of this dag fails.
 ```

The code in your DAG will look something like the following: ([source](https://github.com/apache/airflow/blob/v1-10-stable/airflow/utils/email.py#L41)):

 ```
 from airflow.models.email import send_email

def new_email_alert(self, **kwargs):
  title = "TEST MESSAGE: THIS IS A MODIFIED TEST"
  body = ("I've now modified the email alert "
                "to say whatever I want it to say.<br>")
  send_email('my_email@email.com', title, body)
  ```
