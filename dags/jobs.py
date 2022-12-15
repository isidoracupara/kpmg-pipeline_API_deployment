from datetime import datetime, timedelta
from airflow import DAG
import os
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = {
'owner'                 : 'airflow',
'description'           : 'Use of the DockerOperator',
'depend_on_past'        : False,
'start_date'            : datetime(2021, 5, 1),
'email_on_failure'      : False,
'email_on_retry'        : False,
'retries'               : 1,
'retry_delay'           : timedelta(minutes=5)
}

with DAG('docker_operator_demo', default_args=default_args, schedule_interval="5 * * * *", catchup=False) as dag:
    start_dag = DummyOperator(
        task_id='start_dag'
        )

    end_dag = DummyOperator(
        task_id='end_dag'
        )        

    t1 = BashOperator(
        task_id='scrape_for_pdf',
        bash_command='echo "IN: Scraping website\nOUT: PDF"'
        )
        
    t2 = BashOperator(
        task_id='extract_pdf_text',
        bash_command='echo "IN: PDF\nOUT: Extracted text + sending it to DB"'
        )
    t3 = BashOperator(
        task_id='process_text_data',
        bash_command='echo "Get the text from database and process it with a model?'
        )

    start_dag >> t1 
    
    t1 >> t2

    t2 >> t3

    t3 >> end_dag