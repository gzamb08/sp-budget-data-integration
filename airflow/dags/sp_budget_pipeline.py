import sys
import os
sys.path.insert(1, '.')

from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.docker_operator import DockerOperator


default_args = {
    "owner": "engenharia-dados",
    "depends_on_past": False,
    "start_date": datetime(2021,1,1),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}

with DAG("sp_budget_pipeline",
         default_args=default_args,
         schedule_interval=None,
         catchup=False,
         tags=["etl-engine"]) as dag:

    dummy_start = DummyOperator(
        task_id='start',
        dag=dag
    )

    checkpoint = DummyOperator(
        task_id='checkpoint',
        dag=dag
    )

    ingestion_sources = ['gdvDespesasExcel', 'gdvReceitasExcel']
    app_sources = ['sp_budget']

    def generate_docker_operator(source: str,
                                 engine: str):

        return DockerOperator(
            task_id=f'{engine}-{source}',
            image='etl-engine:latest',
            container_name=f'etl-engine___{engine}-{source}',
            api_version='auto',
            auto_remove='force',
            environment={
                'ENGINE': engine,
                'SOURCE': source
            },
            docker_url="unix://var/run/docker.sock",
            network_mode="bridge"
        )

    for source in ingestion_sources:
        dummy_start >> generate_docker_operator(source, 'ingestion') >> checkpoint
    for source in app_sources:
        checkpoint >> generate_docker_operator(source, 'app')