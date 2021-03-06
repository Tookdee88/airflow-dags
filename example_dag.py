from datetime import datetime, timedelta
from random import randint

import numpy as np

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
    schedule_interval=None,
    max_active_runs=5,
    concurrency=10
)


# Generate 300 tasks
tasks = ["task{}".format(i) for i in range(1, 101)]
example_dag_complete_node = DummyOperator(task_id="example_dag_complete", dag=dag)

org_dags = []
for task in tasks:

    my_templated_command = 'touch test.py; echo "import numpy as np" >> test.py; echo "np.ones((2 ** 29), dtype=np.uint8)" >> test.py; python test.py;'


    org_node = BashOperator(
        task_id="{}".format(task),
        bash_command=my_templated_command,
        wait_for_downstream=False,
        pool='example',
        retries=5,
        dag=dag
    )
    org_node.set_downstream(example_dag_complete_node)
