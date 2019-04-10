# Migrating to Astronomer v0.8
_Moving from Astronomer v0.7.5 to Astronomer v0.8

Astronomer v0.8.0 is full of new features that make the user experience better as well as set the stage for features we're building out in the future. Unfortunately, due to the fact that we had to rewrite our API for this release, upgrading is going to be a bit of a more manual process.

We'll walk through migrating all your DAG data to your new environment in this guide.

**Note:** You can only migrate over Postgres data for instances running Airflow 1.10.1


1) Backup your database.
Most managed databases (RDS, CloudSQL, etc.) are automatically backed up at a regular interval, but it might help to do so manually just incase.

2) Verify that you can connect and query your Airflow database.
We'll need to pull the information out of it and upload it to your new database. Your database might have a master username/password that has access to all of the Airflow databases on your Postgres instance.  

3) Turn off all of your dags

4) Download the info from your Airflow deployments using `pg_dump`

```
pg_dump --host={host} --dbname={dbname} --schema=airflow --data-only --blobs --username={username} --file={pg_dump_file_path} --table=connection --table=dag --table=dag_pickle --table=dag_run --table=dag_stats --table=import_error --table=known_event --table=sla_miss --table=slot_pool --table=task_fail --table=task_instance --table=task_reschedule --table=variable --table=xcom
```

This grabs the `dag`, `dag_pickle`, `dag_run`, `dag_stats`, `import_error`, `known_event`, `sla_miss`, `slot_pool`, `task_fail`, `task_instance`, and `task_reschedule` tables.

**This cannot be used to migrate the `users` table.**

You'll want to run this for each of your Airflow deployments you are looking to migrate.

5) Get the fernet key from your old install. 
`kubectl get secret {old deployment name}-fernet-key -o yaml`
Copy the value after fernet-key: somewhere safe. This will be applied to the new install a few steps below.

6) Delete your old Astronomer Platform, **not** the Airflow deployment.
`helm delete --purge [PLATFORM RELEASE NAME]`

**Note**: If you are simply moving everything over to a new cluster, you can skip this step.

7) Install Astronomer v0.8 on your cluster:
- Checkout `v0.8.2` of the Astronomer helm chart
- Add a section for SMTP credential in your `config.yaml` in the format
```
astronomer:
  houston:
    config:
      email:
        enabled: true
        smtpUrl: smtps://USER:PW@HOST/?pool=true

```
`helm install -f config.yaml . --namespace astronomer`
You can leave the rest of your `config.yaml` the same.

8) Create an Airflow deployment on your new Astronomer version.

9) Restore your fernet key into the new v8 installation. `kubectl edit secret {new deployment name}-fernet-key -o yaml` This will open the secret for editing in Vi. You will need to remove the value that was created after fernet-key: and replace it with the value you got from step 4 and save. 

**Note: Keep your the fernet key somewhere safe you are replacing until after you are doen with the upgrade as there is no way to recover it**

10) Run pg_restore against the new database created by the v8 install:
```
psql -d {dbname} -c "TRUNCATE TABLE airflow.connection;"
psql {dbname} < /tmp/{pg_dump_file_path}  
```
11) Run `kubectl delete --all pods --namespace=<namespace>` in the namespace your Airflow deployment is in. This will force each of the new pods to pick up the secret.

12 Edit first line of your project's Dockerfile to `FROM astronomerinc/ap-airflow:0.8.2-1.10.2-onbuild`

13) Run `astro upgrade` to ensure you are on the latest version of the CLI

14) Redeploy your code to its corresponding instance.

15) In Admin-> Connections, try editing one of the connections you loaded in to ensure the Fernet key was transferred properly.
