from datetime import datetime, timedelta
from uuid import uuid4
from airflow import DAG
import os
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = {
'owner'                 : 'airflow',
'description'           : 'KPMG use case pipeline',
'depend_on_past'        : False,
'start_date'            : datetime(2021, 5, 1),
'email_on_failure'      : False,
'email_on_retry'        : False,
'retries'               : 1,
'retry_delay'           : timedelta(minutes=5)
}

with DAG('kpmg_use_case', default_args=default_args, catchup=False) as dag:
    pipeline_id = str(uuid4())

    start_dag = DummyOperator(
        task_id='start_dag'
        )

    end_dag = DummyOperator(
        task_id='end_dag'
        )        

    t1 = DockerOperator(
        task_id='scrape_for_pdf',
        image='scraper:latest',
        container_name='scraper_task',
        api_version='auto',
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        environment={
            "AZURE_CONNECTION_STRING": os.getenv("AZURE_CONNECTION_STRING"),
            "STORAGE_CONTAINER": os.getenv("STORAGE_CONTAINER"),
            "PIPELINE_ID": pipeline_id
        }
    )
        
    t2 = DockerOperator(
        task_id='extract_pdf_text',
        image='text_extractor:latest',
        container_name='text_extractor_task',
        api_version='auto',
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        environment={
            "AZURE_CONNECTION_STRING": os.getenv("AZURE_CONNECTION_STRING"),
            "STORAGE_CONTAINER": os.getenv("STORAGE_CONTAINER"),
            "PIPELINE_ID": pipeline_id
        }
    )

    t3 = BashOperator(
        task_id='process_text_data',
        bash_command='echo "Get the text from database and process it with a model?"'
        )

    start_dag >> t1 
    
    t1 >> t2

    t2 >> t3

    t3 >> end_dag