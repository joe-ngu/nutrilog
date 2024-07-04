#!/bin/bash

set -exo pipefail

echo "Waiting for Postgres..."

while ! nc -z postgres 5432; do
	sleep 0.1
done

echo "Postgres started"

python3 migrate.py

uvicorn nutrilog.app:app --reload --host "0.0.0.0" --port "8000"
