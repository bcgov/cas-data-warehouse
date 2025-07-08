# -*- coding: utf-8 -*-
from dag_configuration import default_dag_args
from trigger_k8s_cronjob import trigger_k8s_cronjob
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow import DAG
import os


YESTERDAY = datetime.now() - timedelta(days=1)
TWO_DAYS_AGO = datetime.now() - timedelta(days=2)

namespace = os.getenv('CIIP_NAMESPACE')

import_data_sources_args = {
    **default_dag_args,
    'start_date': YESTERDAY,
    'is_paused_upon_creation': False
}

"""
DAG import_from_ciip
Import CIIP data into theo CAS Data Warehouse.
"""
import_from_ciip = DAG('cas_data_warehouse_ciip_import', schedule_interval=None,
                    default_args=import_data_sources_args)


def ciip_import_step(dag):
    return PythonOperator(
        python_callable=trigger_k8s_cronjob,
        task_id='cas_data_warehouse_ciip_import',
        op_args=['cas-data-warehouse-ciip-import', namespace],
        dag=dag)

def swrs_import_step(dag):
    return PythonOperator(
        python_callable=trigger_k8s_cronjob,
        task_id='cas_data_warehouse_swrs_import',
        op_args=['cas-data-warehouse-swrs-import', namespace],
        dag=dag)


ciip_import_step(import_from_ciip) 
