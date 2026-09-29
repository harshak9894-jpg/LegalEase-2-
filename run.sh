#!/bin/bash
echo "========================================"
echo " Starting LegalEase (Backend + Frontend)"
echo "========================================"

echo "Starting FastAPI Backend on port 8001..."
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8001 &

sleep 2

echo "Starting Streamlit Frontend on port 8501..."
streamlit run frontend/app.py --server.port 8501
