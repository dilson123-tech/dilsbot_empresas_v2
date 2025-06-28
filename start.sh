#!/bin/bash
pip install -r requirements.txt
python3 -m uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-8000}
