#! /bin/sh
gunicorn -b 0.0.0.0:5000 run:app --workers=1 --timeout=500 --log-level=$LOG_LEVEL
