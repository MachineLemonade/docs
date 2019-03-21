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

**However, this cannot be used

You'll want to run this for each of your Airflow deployments you are looking to migrate.

4) Delete your old Astronomer Platform, **not** the Airflow deployment.
`helm delete --purge [PLATFORM RELEASE NAME]`

**Note**: If you are simply moving everything over to a new cluster, you can skip this step.

5) Install Astronomer v0.8 on your cluster.

6) Create an Airflow deployment on your new Astronomer version.

7) Run pg_restore:
```
psql -d {dbname} -c "TRUNCATE TABLE airflow.connection;"
psql {dbname} < /tmp/{pg_dump_file_path}
```

**Note:** This will clear out the `Connections` tab. You'll have to  enter those in again.

8) Redeploy your code to its corresponding instance.
