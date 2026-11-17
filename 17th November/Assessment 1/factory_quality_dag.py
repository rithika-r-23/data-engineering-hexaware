cat > /opt/airflow/dags/factory_quality_dag.py <<'EOF'
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
import csv

def load_batches(): file = open("/opt/airflow/dags/factory_batches.csv", newline=""); rows = list(csv.DictReader(file)); file.close(); print("Batches loaded:", len(rows)); return rows

def check_quality(**context): rows = context["ti"].xcom_pull(task_ids="load_batches"); review = [r["batch_id"] for r in rows if int(r["defective_units"]) > 0.05 * int(r["units_produced"])]; print("Batches requiring review:", review); return review

def calculate_value(**context): rows = context["ti"].xcom_pull(task_ids="load_batches"); total = sum(int(r["units_produced"]) * int(r["value_per_unit"]) for r in rows); print("Total production value:", total); return total

def generate_report(**context): rows = context["ti"].xcom_pull(task_ids="load_batches"); review = context["ti"].xcom_pull(task_ids="check_quality"); total = context["ti"].xcom_pull(task_ids="calculate_value"); print("MANUFACTURING BATCH QUALITY REPORT"); print("----------------------------------"); print("Total batches:", len(rows)); print("Batches requiring review:", review); print("Total production value:", total)

dag = DAG(dag_id="factory_quality_pipeline", start_date=datetime(2025, 1, 1), schedule=None, catchup=False)

load_batches_task = PythonOperator(task_id="load_batches", python_callable=load_batches, dag=dag)
check_quality_task = PythonOperator(task_id="check_quality", python_callable=check_quality, dag=dag)
calculate_value_task = PythonOperator(task_id="calculate_value", python_callable=calculate_value, dag=dag)
generate_report_task = PythonOperator(task_id="generate_report", python_callable=generate_report, dag=dag)

load_batches_task >> [check_quality_task, calculate_value_task]
[check_quality_task, calculate_value_task] >> generate_report_task
EOF