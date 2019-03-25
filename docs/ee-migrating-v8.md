# Migrating to Astronomer v0.8.0
_Moving from Astronomer v0.7.5 to Astronomer v0.8.0_

Astronomer v0.8.0 is full of new features that make the user experience better as well as set the stage for features we're building out in the future. Unfortunately, due to the fact that we had to rewrite our API for this release, upgrading is going to be a bit of a more manual process.

We'll walk through migrating all your DAG data to your new environment in this guide.


1) Backup your database.
Most managed databases (RDS, CloudSQL, etc.) are automatically backed up at a regular interval, but it might help to do so manually just incase.

2) Verify that you can connect and query your Airflow database.
We'll need to pull the information out of it and upload it to your new database. Your database might have a master username/password that has access to all of the Airflow databases on your Postgres instance.  

3) Download the info from your Airflow deployments using `pg_dump`

```
pg_dump --host={host} --dbname={dbname} --schema=airflow --data-only --blobs --username={username} --file={pg_dump_file_path} --table=connection --table=dag --table=dag_pickle --table=dag_run --table=dag_stats --table=import_error --table=known_event --table=sla_miss --table=slot_pool --table=task_fail --table=task_instance --table=task_reschedule --table=variable --table=xcom
```

This grabs the `dag`, `dag_pickle`, `dag_run`, `dag_stats`, `import_error`, `known_event`, `sla_miss`, `slot_pool`, `task_fail`, `task_instance`, and `task_reschedule` tables.

**This cannot be used to migrate the `users` table.**

You'll want to run this for each of your Airflow deployments you are looking to migrate.

4) Get the fernet key from your old install. 
`kubectl get secret {old deployment name}-fernet-key -o yaml`
Copy the value after fernet-key: somewhere safe. This will be applied to the new install a few steps below.

5) Delete your old Astronomer Platform, **not** the Airflow deployment.
`helm delete --purge [PLATFORM RELEASE NAME]`

**Note**: If you are simply moving everything over to a new cluster, you can skip this step.

6) Install Astronomer v0.8 on your cluster.

7) Create an Airflow deployment on your new Astronomer version.

8) Restore your fernet key into the new v8 installation. `kubectl edit secret {new deployment name}-fernet-key -o yaml` This will open the secret for editing in Vi. You will need to remove the value that was created after fernet-key: and replace it with the value you got from step 4 and save. 

9) Run pg_restore:
```
psql -d {dbname} -c "TRUNCATE TABLE airflow.connection;"
psql {dbname} < /tmp/{pg_dump_file_path}  
```

10) Edit first line of your project's Dockerfile to `FROM astronomerinc/ap-airflow:0.8.2-1.10.2-onbuild`

11) Redeploy your code to its corresponding instance.
