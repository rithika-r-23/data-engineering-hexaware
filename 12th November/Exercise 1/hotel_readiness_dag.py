cat > hotel_readiness_dag.py <<'EOF'
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime

def load_rooms(): rooms = [{"room": 101, "status": "Ready", "cleaning_min": 0}, {"room": 102, "status": "Cleaning", "cleaning_min": 25}, {"room": 103, "status": "Ready", "cleaning_min": 0}, {"room": 104, "status": "Cleaning", "cleaning_min": 40}, {"room": 105, "status": "Cleaning", "cleaning_min": 30}]; print("Rooms loaded:", rooms); return rooms

def find_rooms_to_clean(**context): rooms = context["ti"].xcom_pull(task_ids="load_rooms"); to_clean = [r["room"] for r in rooms if r["status"] == "Cleaning"]; print("Rooms to clean:", to_clean); return to_clean

def calculate_cleaning_minutes(**context): rooms = context["ti"].xcom_pull(task_ids="load_rooms"); total = sum(r["cleaning_min"] for r in rooms if r["status"] == "Cleaning"); print("Total cleaning minutes:", total); return total

def generate_housekeeping_report(**context): to_clean = context["ti"].xcom_pull(task_ids="find_rooms_to_clean"); total = context["ti"].xcom_pull(task_ids="calculate_cleaning_minutes"); print("HOUSEKEEPING SUMMARY"); print("--------------------"); print("Rooms needing cleaning:", to_clean); print("Total cleaning time (min):", total)

dag = DAG(dag_id="hotel_readiness_pipeline", start_date=datetime(2025, 1, 1), schedule=None, catchup=False)

load_rooms_task = PythonOperator(task_id="load_rooms", python_callable=load_rooms, dag=dag)
find_rooms_task = PythonOperator(task_id="find_rooms_to_clean", python_callable=find_rooms_to_clean, dag=dag)
calc_minutes_task = PythonOperator(task_id="calculate_cleaning_minutes", python_callable=calculate_cleaning_minutes, dag=dag)
report_task = PythonOperator(task_id="generate_housekeeping_report", python_callable=generate_housekeeping_report, dag=dag)

load_rooms_task >> [find_rooms_task, calc_minutes_task]
[find_rooms_task, calc_minutes_task] >> report_task
EOF