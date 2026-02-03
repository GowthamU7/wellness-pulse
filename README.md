🧠 Wellness Pulse – End-to-End Data Engineering Pipeline

Wellness Pulse is a production-style data engineering project that simulates a consumer health & wellness analytics platform (similar to WebMD / digital health products).
It demonstrates how raw event data is ingested, transformed, validated, and served for analytics using Airflow, dbt, and DuckDB.

🚀 What This Project Does

Generates realistic user behavior, content, and marketing events

Loads raw data into a DuckDB warehouse

Transforms data using dbt (staging → marts)

Enforces data quality checks

Orchestrates everything using Apache Airflow

Runs fully containerized with Docker

🏗️ Architecture Overview

Pipeline Flow

Mock Data Generator (Python)
        ↓
Raw Tables (DuckDB)
  raw.user_events
  raw.health_content
  raw.marketing_events
        ↓
dbt Staging Models
  analytics.stg_user_events
  analytics.stg_health_content
  analytics.stg_marketing_events
        ↓
dbt Marts (Analytics Layer)
  analytics.dim_users
  analytics.dim_content
  analytics.fact_user_daily
  analytics.fact_content_engagement_daily
        ↓
Validated Analytics Tables
(used for dashboards / ML / reporting)

<img width="200" height="506" alt="wellness-pulse" src="https://github.com/user-attachments/assets/aedf2b9a-aa13-4bd9-b002-101171eb1888" />



Orchestration

Apache Airflow DAG runs the full pipeline daily

dbt tests act as a quality gate

Pipeline fails fast if data breaks

🛠️ Tech Stack

Python – data generation & ingestion

DuckDB – analytical data warehouse

dbt – transformations & data quality

Apache Airflow – orchestration

Docker – containerized runtime

▶️ How to Run Locally
Prerequisites

Docker Desktop

Git

Start Airflow
docker compose up -d

Access Airflow UI

URL: http://localhost:8080

Username: admin

Password: admin

Trigger the Pipeline

Open wellness_pulse_pipeline

Click Trigger DAG

All tasks should turn green:

generate_mock_data

load_to_duckdb

dbt_run

dbt_test

✅ Data Quality Checks

Primary keys are not null

Dimension keys are unique

Fact tables reference valid dimensions

Pipeline fails if any test fails

📊 Example Analytics Use Cases

Daily active users

Content engagement trends

Marketing event attribution

Foundation for recommendations / personalization

📸 Screenshots Checklist (Add These)

Airflow DAG graph (all green)

dbt run output

dbt test output

DuckDB tables (analytics.fact_user_daily)


