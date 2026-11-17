cat > /opt/airflow/dags/atm_cash_dag.py <<'EOF'
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
import csv

def load_atms(): file = open("/opt/airflow/dags/atm_cash.csv", newline=""); records = list(csv.DictReader(file)); file.close(); print("ATM records loaded:", len(records)); return records

def identify_low_cash(**context): records = context["ti"].xcom_pull(task_ids="load_atms"); low_cash = [r["atm_id"] for r in records if int(r["cash_available"]) < int(r["daily_demand"])]; print("Low-cash ATMs:", low_cash); return low_cash

def calculate_total_cash(**context): records = context["ti"].xcom_pull(task_ids="load_atms"); total = sum(int(r["cash_available"]) for r in records); print("Total available cash:", total); return total

def generate_report(**context): records = context["ti"].xcom_pull(task_ids="load_atms"); low_cash = context["ti"].xcom_pull(task_ids="identify_low_cash"); total = context["ti"].xcom_pull(task_ids="calculate_total_cash"); print("ATM CASH REPLENISHMENT REPORT"); print("-----------------------------"); print("Number of ATMs:", len(records)); print("Low-cash ATMs:", low_cash); print("Total available cash:", total)

dag = DAG(dag_id="atm_cash_pipeline", start_date=datetime(2025, 1, 1), schedule=None, catchup=False)

load_atms_task = PythonOperator(task_id="load_atms", python_callable=load_atms, dag=dag)
identify_low_cash_task = PythonOperator(task_id="identify_low_cash", python_callable=identify_low_cash, dag=dag)
calculate_total_cash_task = PythonOperator(task_id="calculate_total_cash", python_callable=calculate_total_cash, dag=dag)
generate_report_task = PythonOperator(task_id="generate_report", python_callable=generate_report, dag=dag)

load_atms_task >> [identify_low_cash_task, calculate_total_cash_task]
[identify_low_cash_task, calculate_total_cash_task] >> generate_report_task
EOF