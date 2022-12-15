#!/bin/bash

# Init Airflow
docker compose up airflow-init;
# Run Airflow
# docker-compose --env-file .env up;
docker compose up;