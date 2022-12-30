from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.docker.operators.docker import DockerOperator

with DAG(dag_id="etl_dag",
         start_date=datetime(2022, 12, 29),
         schedule_interval='1 * * * *'
         ) as dag:

    start = EmptyOperator(task_id="start-etl")

    etl_parser = DockerOperator(
        task_id='docker_op_parser',
        # image='de_project_1-parser:latest',
        image='f1050ae41b09231bc79db353ebc26db644b84f9ba739110e3ca7c0520bf7bf2b',
        # container_name='etl_parser',
        # api_version='auto',
        # command="echo ls",
        command=["python", "parser/main.py"],
        docker_url="unix://var/run/docker.sock",
        # network_mode="bridge",
        dag=dag
    )

    etl = DockerOperator(
        task_id='docker_op_etl',
        image='de_project_1-etl:latest',
        # container_name='etl',
        # api_version='auto',
        command=["python", "etl/main.py"],
        docker_url="unix://var/run/docker.sock",
        # network_mode="bridge",
        dag=dag
    )

    start_parser = BashOperator(
        task_id='clean_up_docker',
        bash_command='docker compose up parser',
        dag=dag)

    end = EmptyOperator(task_id="end-etl")

    # start >> etl_parser >> etl >> end
    start >> [etl_parser, etl, start_parser] >> end
