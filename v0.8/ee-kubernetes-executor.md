Kubernetes Executor:

- Solves static allocation issue with Celery
- All task get lauched as pods
- The k8s executor runs a single pod that's running airflow and farms out API calls to k8s.
  - When job is done, the pod spins down
  - since each pod is isolated, can pass in executor configs
- When running via K8s executor, the pods communicate directly with the postgres instance, so scheduler does not have to keep track of that information
- The scheduler reads event stream to see if the pods dies - workers can speak to the postgres directly.
- Scheduler gets status from event stream
- Uses a resourceVersion to recreate state
  - By tracking the event number, when the scheduler goes down, it can pick back up exactly where it left off
  - https://github.com/apache/airflow/blob/master/airflow/executors/kubernetes_executor.py#L396
  - Rereads the event stream from where it goes down
    - Where does it do that from? Does K8s store the event stream for a while?


## Celery Executor

The Kubernetes executor is the next step at running Airflow at scale.

Previously, the Celery Executor required a queue (Redis/RabbitMQ), and statically allocated resources
to scale out Airflow.

## Tasks as Pods

With the K8s executor, the Airflow scheduler farms out API calls to the Kubernetes API to run each task as a Pod. Right off the bat, this allows:
- Dynamic resource allocation. Kubernetes clusters can auto scale up when needed, and then back down when no tasks are running.
- No dependency on an external messaging queue
- Each task can receive specific configurations that will only apply to that specific task. This can be anything from specific environment variables, node pool labels, or resource requests.

## Fault Tolerance

Running each task as a Kubernetes pods makes Airflow a more fault tolerant system for a few reasons:
- Each task talks directly to the database to report state, reducing load on the scheduler. To keep task status, the scheduler reads the Kubernetes event stream.
-  
