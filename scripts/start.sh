#!/bin/bash

# Build docker images
docker build -f dags/kpmg-pipeline/scraper/Dockerfile -t scraper:latest ./dags/kpmg-pipeline;
docker build -f dags/kpmg-pipeline/text_extractor/Dockerfile -t text_extractor:latest ./dags/kpmg-pipeline;
docker build -f API/Dockerfile -t text_extractor:latest ./API;

# Init Airflow
docker compose up airflow-init;
# Run Airflow
docker-compose --env-file .env up;