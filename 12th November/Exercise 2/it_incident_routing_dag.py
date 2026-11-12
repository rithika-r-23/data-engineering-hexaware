cat > /opt/airflow/dags/it_incident_routing_dag.py <<'EOF'
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator, BranchPythonOperator
from datetime import datetime, timedelta

def fail(msg): raise Exception(msg)

def load_incident(): incident = {"ticket_id": "INC-402", "service": "Email", "severity": "High", "reported_by": "Operations"}; print("Incident loaded:", incident); return incident

def choose_response(**context): incident = context["ti"].xcom_pull(task_ids="load_incident"); return "urgent_response" if incident["severity"] in ("High", "Critical") else "standard_response"

def urgent_response(**context): attempt = context["ti"].try_number; print("Urgent response attempt:", attempt); attempt == 1 and fail("Simulated failure: escalation system unavailable"); print("ESCALATION: Incident sent to on-call engineering team")

def standard_response(): print("Incident assigned to the service desk queue")

def write_audit(**context): incident = context["ti"].xcom_pull(task_ids="load_incident"); print("AUDIT LOG"); print("Incident ID:", incident["ticket_id"]); print("Incident handling completed")

dag = DAG(dag_id="it_incident_routing_pipeline", start_date=datetime(2025, 1, 1), schedule=None, catchup=False)

load_incident_task = PythonOperator(task_id="load_incident", python_callable=load_incident, dag=dag)
choose_response_task = BranchPythonOperator(task_id="choose_response", python_callable=choose_response, dag=dag)
urgent_response_task = PythonOperator(task_id="urgent_response", python_callable=urgent_response, retries=1, retry_delay=timedelta(seconds=15), dag=dag)
standard_response_task = PythonOperator(task_id="standard_response", python_callable=standard_response, dag=dag)
write_audit_task = PythonOperator(task_id="write_audit", python_callable=write_audit, trigger_rule="none_failed_min_one_success", dag=dag)

load_incident_task >> choose_response_task
choose_response_task >> [urgent_response_task, standard_response_task]
[urgent_response_task, standard_response_task] >> write_audit_task
EOF