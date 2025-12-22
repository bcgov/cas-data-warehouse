# -*- coding: utf-8 -*-
from dag_configuration import default_dag_args
from trigger_k8s_cronjob import trigger_k8s_cronjob
from airflow.decorators import dag, task
from datetime import datetime, timedelta
import os


YESTERDAY = datetime.now() - timedelta(days=1)
TWO_DAYS_AGO = datetime.now() - timedelta(days=2)
DATA_WAREHOUSE_IMPORT_DAG_NAME = 'cas_data_warehouse_import_data_sources'

namespace = os.getenv('CIIP_NAMESPACE')

import_data_sources_args = {
    **default_dag_args,
    'start_date': YESTERDAY,
    'is_paused_upon_creation': False
}

DATA_WAREHOUSE_IMPORT_DAG_DOC = """
Import data sources into CAS Data Warehouse.
"""

@dag(
    dag_id=DATA_WAREHOUSE_IMPORT_DAG_NAME,
    default_args=import_data_sources_args,
    schedule="0 8 * * *",
    start_date=TWO_DAYS_AGO,
    doc_md=DATA_WAREHOUSE_IMPORT_DAG_DOC,
)
def import_data_sources():
    @task
    def ciip_import_step():
        trigger_k8s_cronjob('cas-data-warehouse-ciip-import', namespace)

    @task
    def swrs_import_step():
        trigger_k8s_cronjob('cas-data-warehouse-swrs-import', namespace)

    @task
    def bciers_import_step():
        trigger_k8s_cronjob('cas-data-warehouse-bciers-import', namespace)

    ciip_import_step() >> swrs_import_step() >> bciers_import_step()

import_data_sources()
