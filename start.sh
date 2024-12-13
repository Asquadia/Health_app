#!/bin/bash
set -e
source /app/venv/bin/activate
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app &
gunicorn -w 4 -b 0.0.0.0:5001 bmi_service.bmi:app &
gunicorn -w 4 -b 0.0.0.0:5002 bmr_service.bmr:app &
wait
