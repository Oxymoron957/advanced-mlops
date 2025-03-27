from datetime import datetime, timedelta
from textwrap import dedent

import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator

from utils.callbacks import failure_callback, success_callback

local_timezone = pendulum.timezone("Asia/Seoul")

with DAG(
    # TODO: "simple_dag"이라는 이름의 DAG 설정
    dag_id="simple_dag",
    default_args={
        "owner": "user",
        "depends_on_past": None,
        "email": "exaple@example.com",
        "email_on_failure": None,
        "email_on_retry": None,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        "on_failure_callback": failure_callback,
        "on_success_callback": success_callback,
    },
    description="Simple airflow dag",
    schedule="0 15 * * *",
    start_date=datetime(2025, 3, 1, tzinfo=local_timezone),
    catchup=False,
    tags=["lgcns", "mlops"],
) as dag:
    task1 = BashOperator(
        task_id="print_date",
        bash_command="date"
    )
    task2 = BashOperator(
        task_id="sleep",
        depends_on_past=False,
        bash_command="sleep 5",
        retries=3
    )

    loop_command = dedent(
        """
        {% for i in range(5) %}
            echo "ds = {{ ds }}"
            echo "macros.ds_add(ds, {{ i }}) = {{ macros.ds_add(ds, i) }}"
        {% endfor %}
        """
    )
    task3 = BashOperator(
        task_id="print_with_loop",
        bash_command=loop_command,
    )

    task1 >> [task2, task3]
