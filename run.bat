@echo off
echo ========================================
echo  Starting LegalEase (Backend + Frontend)
echo ========================================

SET PY_BIN=python
IF EXIST "venv\Scripts\python.exe" SET PY_BIN=venv\Scripts\python.exe
IF EXIST ".venv\Scripts\python.exe" (
    venv\Scripts\python.exe --version >nul 2>&1
    IF ERRORLEVEL 1 (
        IF EXIST ".venv\Scripts\python.exe" SET PY_BIN=.venv\Scripts\python.exe
    )
)

SET ST_BIN=streamlit
IF EXIST "venv\Scripts\streamlit.exe" SET ST_BIN=venv\Scripts\streamlit.exe
IF EXIST ".venv\Scripts\streamlit.exe" (
    venv\Scripts\streamlit.exe --version >nul 2>&1
    IF ERRORLEVEL 1 (
        IF EXIST ".venv\Scripts\streamlit.exe" SET ST_BIN=.venv\Scripts\streamlit.exe
    )
)

echo Starting FastAPI Backend on port 8001...
start "LegalEase Backend" %PY_BIN% -m uvicorn legalEaseAPI.main:app --host 127.0.0.1 --port 8001 --reload

timeout /t 2 /nobreak >nul

echo Starting Streamlit Frontend on port 8501...
%ST_BIN% run frontend/app.py --server.port 8501
