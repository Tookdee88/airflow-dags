from datetime import datetime, timedelta
from random import randint

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'start_date': days_ago(0),
    'catchup': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'example_dag',
    default_args=default_args,
    schedule_interval=timedelta(minutes=30),
    max_active_runs=5,
    concurrency=10
)

# Generate 300 tasks
tasks = ["task{}".format(i) for i in range(1, 101)]
example_dag_complete_node = DummyOperator(task_id="example_dag_complete", dag=dag)

org_dags = []
for task in tasks:

    bash_command = "python -c '[x^10 for x in range(1,100000000)]'"

    org_node = BashOperator(
        task_id="{}".format(task),
        bash_command=bash_command,
        wait_for_downstream=False,
        pool='example',
        retries=5,
        dag=dag
    )
    org_node.set_downstream(example_dag_complete_node)
