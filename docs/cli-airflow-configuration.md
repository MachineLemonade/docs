---
title: "Adding Airflow Configuration with Astro CLI"
description: "Set up connections, variables, and pools automatically with the Astronomer CLI."
link: "Adding Airflow Configuration"
date: 2019-01-31T00:00:00.000Z
slug: "cli-airflow-configuration"
---

One of the most useful features of the Astro CLI during development is the ability to have connections, variables, and pools automatically generated on `astro airflow start`. Using this feature, you can kill your environment and automatically start back up with all of your necessary configuration to start again.

**NOTE**: Connections, variables, and pools defined through this process will only be available locally. To ensure they are available in your remote deployments, please add them via the Airflow UI.

## settings.yaml
When you first `astro airflow init` to create a new project, a file titled `settings.yaml` will be created to add connections, pools, and variables. By default, the structure within this file will look like the following:

```
airflow:
  connections:
    - conn_id: my_new_connection
      conn_type: postgres
      conn_host: 123.0.0.4
      conn_login: user
      conn_password: pw
      conn_port: 5432
      conn_extra:
  pools:
    - pool_name: my_new_pool
      pool_slot: 5
      pool_description:
  variables:
    - variable_name: my_variable
      variable_value: my_value
```

If you want to add a second connection/pool/variable, simply copy the existing fields and make a new entry like so:

```
variables:
  - variable_name: my_first_variable
    variable_value: value123
  - variable_name: my_second_variable
    variable_value: value987
```

## Usage
Once you have filled out your settings, they will be added to your Airflow instance on `astro airflow start`. If you have any connections, pools, or variables with the same name as those defined in `settings.yaml`, those will be overwritten.

```
$ astro-local airflow start
Sending build context to Docker daemon  24.58kB
Step 1/1 : FROM astronomerinc/ap-airflow:0.7.5-1.9.0-onbuild
# Executing 5 build triggers
 ---> Using cache
 ---> Using cache
 ---> Using cache
 ---> Using cache
a ---> 08133ce1aed2
Successfully built 08133ce1aed2
Successfully tagged another-test/airflow:latest
INFO[0000] [0/3] [postgres]: Starting                   
INFO[0001] [1/3] [postgres]: Started                    
INFO[0001] [1/3] [scheduler]: Starting                  
INFO[0002] [2/3] [scheduler]: Started                   
INFO[0002] [2/3] [webserver]: Starting                  
INFO[0003] [3/3] [webserver]: Started                   
Added Connection: my_new_connection
Added Pool: my_new_pool
Added Variable: my_variable
Airflow Webserver: http://localhost:8080/admin/
Postgres Database: localhost:5432/postgres
```

For connections, if conn_type or conn_uri is not specified, that connection will be skipped.
```
Skipping my_new_connection: ConnType or ConnUri must be specified.
```

For pools, if a pool_slot has not been set, that pool will be skipped.
```
Skipping my_new_pool: Pool Slot must be set.
```

For variables, you may set a variable with a name and no value but if there is a value with no variable name, it will be skipped.
```
Skipping Variable Creation: No Variable Name Specified.
```

**Note:** If putting in a dict for any value, this will need to be wrapped in single quotes for the yaml to be successfully parsed.
